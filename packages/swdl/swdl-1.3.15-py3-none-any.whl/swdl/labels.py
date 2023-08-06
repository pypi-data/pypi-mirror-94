import json
from base64 import b64encode, b64decode

import h5py as h5
import numpy as np
from google.api_core.exceptions import NotFound, TooManyRequests
from google.cloud import storage

CP_FRAMERATE = 25
CP_DIM = 4
CP_INTERVAL = 10


class CameraPositionError(Exception):
    pass


class InvalidCameraPositionError(CameraPositionError):
    pass


def round_timestamps(array: np.ndarray):
    if array is None:
        return None
    output = np.zeros([CP_FRAMERATE * CP_INTERVAL, CP_DIM], np.float32)
    rounded_ts = np.round(array[:, 0] * CP_FRAMERATE) / CP_FRAMERATE
    array_index = np.round((rounded_ts % CP_INTERVAL) * CP_FRAMERATE).astype(int)
    array_index[array[:, 0] == 0] = -1
    for i, ts in enumerate(array_index):
        if ts == -1:
            continue
        output[ts] = array[i]
        output[ts, 0] = round(output[ts, 0] * CP_FRAMERATE) / CP_FRAMERATE
    return output


def merge_arrays(old: np.ndarray, new: np.ndarray) -> np.ndarray:
    if old is None:
        return new
    for i, item in enumerate(new):
        if item[0] != 0:
            old[i] = item
    return old


def get_segment_indeces(np_data):
    rounded_ts = np.round(np_data[:, 0] * CP_FRAMERATE) / CP_FRAMERATE
    time_indexes = (rounded_ts // CP_INTERVAL).astype(int)
    return time_indexes


class CPManager:
    """Tool to savely push camera positions to a cloud bucket"""

    def __init__(self, bucket_name):
        """
        Args:
            bucket_name: The bucket name
        """
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def _get_manifest(self, match_id: str, virtual_cam_id: int):
        manifest_path = f"{match_id}/camera_positions/{virtual_cam_id}/cp.json"
        blob = self.bucket.blob(manifest_path)
        try:
            manifest_string = blob.download_as_string()
        except NotFound:
            manifest_string = None
        if not manifest_string:
            return None
        try:
            return json.loads(manifest_string)
        except json.JSONDecodeError:
            return None

    def _upload_manifest(self, manifest: dict, match_id: str, virtual_cam_id: int):
        for i in range(5):
            try:
                manifest_path = f"{match_id}/camera_positions/{virtual_cam_id}/cp.json"
                blob = self.bucket.blob(manifest_path)
                blob.cache_control = "no-cache,no-store,must-revalidate,max-age=0"
                blob.upload_from_string(json.dumps(manifest))
                break
            except TooManyRequests:
                pass

    def _upload_segment(
        self, data: bytes, match_id: str, virtual_camera_id: int, time_id: int
    ):

        upload_path = f"{match_id}/camera_positions/{virtual_camera_id}/{time_id}.cp"
        for i in range(5):
            try:
                blob = self.bucket.blob(upload_path)
                blob.cache_control = "no-cache,no-store,must-revalidate,max-age=0"
                blob.upload_from_string(data)
                break
            except TooManyRequests:
                pass

    def upload_data(self, cam_data: bytes, match_id: str, virtual_cam_id: int):
        """Push the camera positions to the bucket
        Args:
            cam_data: The camera positions. Must be a base64 encoded float32 array
            match_id: The camera id
            virtual_cam_id: The virtual camera id

        """

        try:
            np_data = np.frombuffer(b64decode(cam_data), np.float32).reshape(-1, CP_DIM)
        except ValueError:
            raise InvalidCameraPositionError(
                f"The provided data data seems not to contain valid camera positions. "
                f"Make sure your data array is of shape (None, {CP_DIM}), 32bit float "
                f"and is base64 encoded."
            )
        time_indexes = get_segment_indeces(np_data)
        time_idx_set = list(set(time_indexes))
        for time_id in sorted(time_idx_set):
            data = np_data[time_indexes == time_id]

            upload_path = f"{match_id}/camera_positions/{virtual_cam_id}/{time_id}.cp"
            blob = self.bucket.blob(upload_path)
            try:
                existing_data = blob.download_as_string()
                existing_data = np.frombuffer(
                    b64decode(existing_data), np.float32
                ).reshape([-1, CP_DIM])
            except (NotFound, ValueError):
                existing_data = None

            data = round_timestamps(data)
            existing_data = round_timestamps(existing_data)
            data = merge_arrays(existing_data, data)
            cam_data = b64encode(data.tobytes())
            self._upload_segment(cam_data, match_id, virtual_cam_id, time_id)

        new_max = int(max(time_idx_set))
        manifest = self._get_manifest(match_id, virtual_cam_id)
        if manifest:
            if "max_index" in manifest:
                old_max = manifest["max_index"]
                if new_max <= old_max:
                    return

        manifest = {
            "max_index": new_max,
            "framerate": CP_FRAMERATE,
            "interval": CP_INTERVAL,
            "dimensions": CP_DIM,
        }
        self._upload_manifest(manifest, match_id, virtual_cam_id)


class Label:
    """
    Structure to store label data, just wraping numpy arrays
    """

    def __init__(self):
        self.positions_dim = 8
        self.events = np.zeros((0, 3), dtype=np.uint32)
        self.status = np.zeros((11,), dtype=np.uint32)
        self.positions = np.zeros((0, self.positions_dim), dtype=np.float32)
        self.player_positions = {0: np.zeros((25, 3), dtype=np.float32)}
        self.label_resolution = 250

    @classmethod
    def from_file(cls, path="labels.h5"):
        """
        Reads from hdf5 file

        # Attributes
        path(str):
        """
        file = h5.File(path, "r")
        label = cls()
        label.positions = file["labels"][:]
        label.events = file["events"][:]
        label.status = file["status"][:]
        file.close()
        return label

    def save(self, path="labels.h5"):
        """
        Saves label to hdf5

        # Attributes
        path(str):
        """
        file = h5.File(path, "w")
        file["events"] = self.events
        file["labels"] = self.positions
        file["status"] = self.status
        file.close()

    def set_position(self, timestamp, target_position, actual_position, auto=1):
        """
        Adds a position to the given timestamp

        # Arguments:
        timestamp (int): video time in ms
        target_position (array): x, y and z where the camera should look at
        actual_position (array): x, y and z where the camera actually looking
        at
        """
        row = int(timestamp / self.label_resolution)
        if self.positions.shape[0] < row + 1:
            self.positions.resize((row + 1, self.positions_dim), refcheck=False)
        a = actual_position
        t = target_position
        item = [row * self.label_resolution, t[0], t[1], t[2], a[0], a[1], a[2], auto]
        self.positions[row] = item
