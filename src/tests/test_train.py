import src.main as main


class _FakeExecutor:
    def __init__(self, map_return=None):
        self.map_return = map_return or []
        self.map_calls = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def map(self, func, slice_files, output_paths):
        self.map_calls.append((func, list(slice_files), list(output_paths)))
        return iter(self.map_return)


def test_run_full_etl_processes_only_json_files(monkeypatch):
    fake_executor = _FakeExecutor(map_return=[3, 5])

    monkeypatch.setattr(main, "DATASET_PATH", "/tmp/dataset")
    monkeypatch.setattr(main, "PROCESSED_DATA_PATH", "/tmp/output")
    monkeypatch.setattr(main.os, "listdir", lambda _: ["a.json", "b.txt", "c.json"])
    monkeypatch.setattr(main, "ProcessPoolExecutor", lambda: fake_executor)

    logs = []
    monkeypatch.setattr(main.logger, "info", lambda msg: logs.append(msg))

    main.run_full_etl()

    assert len(fake_executor.map_calls) == 1
    func, slice_files, output_paths = fake_executor.map_calls[0]
    assert func is main.load_tracks
    assert slice_files == ["/tmp/dataset/a.json", "/tmp/dataset/c.json"]
    assert output_paths == ["/tmp/output", "/tmp/output"]
    assert any("Processed 8 total tracks across all slices." in m for m in logs)


def test_run_full_etl_with_no_json_files(monkeypatch):
    fake_executor = _FakeExecutor(map_return=[])

    monkeypatch.setattr(main, "DATASET_PATH", "/tmp/dataset")
    monkeypatch.setattr(main, "PROCESSED_DATA_PATH", "/tmp/output")
    monkeypatch.setattr(main.os, "listdir", lambda _: ["note.txt", "readme.md"])
    monkeypatch.setattr(main, "ProcessPoolExecutor", lambda: fake_executor)

    logs = []
    monkeypatch.setattr(main.logger, "info", lambda msg: logs.append(msg))

    main.run_full_etl()

    assert len(fake_executor.map_calls) == 1
    _, slice_files, output_paths = fake_executor.map_calls[0]
    assert slice_files == []
    assert output_paths == []
    assert any("Processed 0 total tracks across all slices." in m for m in logs)


def test_run_train_logs_start(monkeypatch):
    logs = []
    monkeypatch.setattr(main.logger, "info", lambda msg: logs.append(msg))

    result = main.run_train()

    assert result is None
    assert any("Starting training process..." in m for m in logs)
