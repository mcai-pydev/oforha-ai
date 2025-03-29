# Oforha.ai

A modern web platform for AI research, development, and education. This repository contains the frontend implementation of the Oforha.ai website.

## Features

- Modern, responsive design
- Dark/light theme support
- Interactive neural network visualization
- Project showcase
- Research papers section
- Contact form
- Mobile-friendly navigation

## Project Structure

```
oforha.ai/
├── assets/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       ├── favicon.svg
│       ├── neural-network.svg
│       └── projects/
│           └── ai-ml-insights.svg
└── index.html
```

## Technologies Used

- HTML5
- CSS3 (with CSS Variables and Flexbox/Grid)
- JavaScript (ES6+)
- SVG for graphics and animations
- Font Awesome for icons
- Google Fonts (Inter)

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/mcai-pydev/oforha.ai.git
   ```

2. Navigate to the project directory:
   ```bash
   cd oforha.ai
   ```

3. Open `index.html` in your web browser or use a local development server.

## Development

### Adding New Projects

1. Create a new SVG image in `assets/images/projects/`
2. Add a new project card in the projects section of `index.html`
3. Update the project links and descriptions

### Adding Research Papers

1. Add a new research card in the research section of `index.html`
2. Link to the research paper or documentation
3. Update the description and tags

### Customizing the Theme

The website uses CSS variables for theming. You can modify the colors in `style.css`:

```css
:root {
    --primary: #0366d6;
    --secondary: #2ea44f;
    --dark: #24292e;
    --light: #f6f8fa;
    --text: #586069;
    --gradient-start: #0a2540;
    --gradient-end: #1a365d;
}
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any questions or suggestions, please contact us at contact@oforha.ai or open an issue in the repository. 