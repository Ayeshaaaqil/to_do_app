# Todo App with Tailwind CSS

This project demonstrates two different ways to set up Tailwind CSS in a simple Todo application.

## Method 1: CDN Setup (Easiest)

The file `todo_app_cdn.html` uses Tailwind via CDN. This is the quickest way to get started:

```html
<script src="https://cdn.tailwindcss.com"></script>
```

To use this method:
1. Open `todo_app_cdn.html` directly in your browser
2. Tailwind classes should work immediately

## Method 2: NPM Setup (Recommended for production)

This setup processes Tailwind classes at build time, resulting in smaller CSS files.

### Setup Instructions:

1. Install dependencies:
```bash
npm install
```

2. Build Tailwind CSS:
```bash
npm run build
```

3. Or watch for changes during development:
```bash
npm run watch
```

4. Open `todo_app_npm.html` in your browser

### Files included:
- `todo_app_npm.html` - The HTML file that uses Tailwind classes
- `src/input.css` - The source CSS file with Tailwind directives
- `tailwind.config.js` - Configuration file for Tailwind
- `package.json` - Contains build scripts and dependencies

## Troubleshooting Common Issues

### 1. Tailwind classes not working
- **CDN method**: Make sure the CDN script is included before any elements that use Tailwind classes
- **NPM method**: Ensure you've run the build command and the output CSS file is linked in your HTML

### 2. Content not being processed
- **NPM method**: Verify your HTML files are listed in the `content` array in `tailwind.config.js`

### 3. Build issues
- Make sure Node.js is installed on your system
- Try clearing npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules package-lock.json && npm install`

### 4. Caching issues
- Hard refresh your browser (Ctrl+Shift+R or Cmd+Shift+R)
- Clear browser cache
- Try opening in an incognito/private window

## Testing if Tailwind is Working

Both HTML files include visual elements that will clearly show if Tailwind is working:
- Colored background (`bg-indigo-600`)
- Rounded corners (`rounded-lg`)
- Shadows (`shadow-md`)
- Flexbox utilities (`flex`, `items-center`)
- Spacing (`p-6`, `mb-6`, etc.)

If you see styled elements (colors, rounded corners, proper spacing), Tailwind is working correctly.