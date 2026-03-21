import src.train as train


class _FakeExecutor:
    def __init__(self, map_return=None):
        self.map_return = map_return or []
        self.map_calls = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def map(self, func, slice_files, output_paths, limits):
        self.map_calls.append((func, list(slice_files), list(output_paths), list(limits)))
        return iter(self.map_return)


def test_run_full_etl_processes_only_json_files(monkeypatch):
    fake_executor = _FakeExecutor(map_return=[3, 5])

    monkeypatch.setattr(train, "DATASET_PATH", "/tmp/dataset")
    monkeypatch.setattr(train, "PROCESSED_DATA_PATH", "/tmp/output")
    monkeypatch.setattr(train, "LIMIT", 7)
    monkeypatch.setattr(train.os, "listdir", lambda _: ["a.json", "b.txt", "c.json"])
    monkeypatch.setattr(train, "ProcessPoolExecutor", lambda: fake_executor)

    logs = []
    monkeypatch.setattr(train.logger, "info", lambda msg: logs.append(msg))

    train.run_full_etl()

    assert len(fake_executor.map_calls) == 1
    func, slice_files, output_paths, limits = fake_executor.map_calls[0]
    assert func is train.load_tracks
    assert slice_files == ["/tmp/dataset/a.json", "/tmp/dataset/c.json"]
    assert output_paths == ["/tmp/output", "/tmp/output"]
    assert limits == [7, 7]
    assert any("Processed 8 total tracks across all slices." in m for m in logs)


def test_run_full_etl_with_no_json_files(monkeypatch):
    fake_executor = _FakeExecutor(map_return=[])

    monkeypatch.setattr(train, "DATASET_PATH", "/tmp/dataset")
    monkeypatch.setattr(train, "PROCESSED_DATA_PATH", "/tmp/output")
    monkeypatch.setattr(train, "LIMIT", 2)
    monkeypatch.setattr(train.os, "listdir", lambda _: ["note.txt", "readme.md"])
    monkeypatch.setattr(train, "ProcessPoolExecutor", lambda: fake_executor)

    logs = []
    monkeypatch.setattr(train.logger, "info", lambda msg: logs.append(msg))

    train.run_full_etl()

    assert len(fake_executor.map_calls) == 1
    _, slice_files, output_paths, limits = fake_executor.map_calls[0]
    assert slice_files == []
    assert output_paths == []
    assert limits == []
    assert any("Processed 0 total tracks across all slices." in m for m in logs)


def test_run_train_logs_start(monkeypatch):
    logs = []
    monkeypatch.setattr(train.logger, "info", lambda msg: logs.append(msg))

    result = train.run_train()

    assert result is None
    assert any("Starting training process..." in m for m in logs)
