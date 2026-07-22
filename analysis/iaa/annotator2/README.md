# Annotator-2 deposits

Place completed segment CSVs here:

```text
segments/<athlete>/<video_basename>.csv
```

or:

```text
segments/master_segment_labels_annotator2.csv
```

Do **not** commit unfinished drafts with invented labels.

When complete, run:

```bash
python scripts/compute_iaa_agreement.py
```

See `docs/annotation/IAA_PROTOCOL.md`.
