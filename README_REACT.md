# Human Detection Form React Component

A reusable React component that replicates the functionality of the existing HTML form for human detection in disaster scenarios.

## Features

- File upload for images/videos
- Confidence threshold slider with live value display
- Loading states during processing
- Results display for both images and videos
- Responsive design with Tailwind CSS
- Self-contained and reusable

## Installation

1. Copy `HumanDetectionForm.jsx` to your React project's components directory
2. Make sure you have Tailwind CSS configured in your project

## Usage

```jsx
import HumanDetectionForm from './components/HumanDetectionForm';

function App() {
  return (
    <div className="App">
      <HumanDetectionForm />
    </div>
  );
}
```

## Component Structure

The component manages all its own state internally:
- `file`: The selected file for upload
- `confidence`: Confidence threshold value (0.1-1.0)
- `isSubmitting`: Loading state during processing
- `result`: Processed results to display
- `error`: Error messages

## Styling

The component uses Tailwind CSS classes for all styling. Make sure your project has Tailwind configured properly.

## Customization

You can customize the component by:
1. Modifying the Tailwind classes directly
2. Passing props to configure behavior
3. Extending the component with additional features

## Note

This is a UI-only component. To integrate with a backend API, you would need to replace the mock processing logic in the `handleSubmit` function with actual API calls.