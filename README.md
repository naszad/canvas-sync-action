# Canvas Sync GitHub Action

Syncs repository content to Canvas LMS, maintaining the repository structure.

## Usage

1. Add Canvas credentials to repository secrets:
```yaml
CANVAS_API_URL: "https://canvas.instructure.com"
CANVAS_API_KEY: "your-api-key"
CANVAS_COURSE_ID: "your-course-id"
```

2. With the following format, create `.github/workflows/canvas-sync.yml`:
```yaml
name: Sync to Canvas
on:
  push:
    branches: [ "main" ]
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: naszad/canvas-sync-action@v1.0.0
        with:
          canvas_api_url: ${{ secrets.CANVAS_API_URL }}
          canvas_api_key: ${{ secrets.CANVAS_API_KEY }}
          canvas_course_id: ${{ secrets.CANVAS_COURSE_ID }}
```

## License

MIT
