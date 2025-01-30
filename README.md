# Canvas Sync GitHub Action

This action syncs your GitHub repository content to Canvas LMS, maintaining the repository structure and automatically updating files when changes are pushed.

## Features

- Automatically syncs repository content to Canvas
- Maintains folder structure
- Uses repository name as the root folder in Canvas
- Updates files on push to main branch

## Usage

1. First, set up your Canvas API credentials in your repository's secrets:

   - `CANVAS_API_URL`: Your Canvas instance URL
   - `CANVAS_API_KEY`: Your Canvas API key
   - `CANVAS_COURSE_ID`: The ID of your Canvas course

2. Create a workflow file (e.g., `.github/workflows/canvas-sync.yml`):

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
      - name: Sync to Canvas
        uses: yourusername/canvas-sync-action@v1
        with:
          canvas_api_url: ${{ secrets.CANVAS_API_URL }}
          canvas_api_key: ${{ secrets.CANVAS_API_KEY }}
          canvas_course_id: ${{ secrets.CANVAS_COURSE_ID }}
```

## Inputs

| Input | Description | Required |
|-------|-------------|----------|
| `canvas_api_url` | Your Canvas instance URL | Yes |
| `canvas_api_key` | Your Canvas API key | Yes |
| `canvas_course_id` | The ID of your Canvas course | Yes |

## Example

When you push changes to your main branch, the action will:

1. Create a folder in Canvas with your repository name
2. Replicate your repository's folder structure
3. Upload all files while maintaining the hierarchy
4. Update any changed files on subsequent pushes

## License

MIT
