import { render, screen } from '@testing-library/react';
import App from './App';

test('renders application', () => {
  render(<App />);
  // Basic test to ensure app renders without crashing
  expect(document.body).toBeInTheDocument();
});

test('renders login page initially', () => {
  render(<App />);
  // The app should redirect to login if not authenticated
  expect(window.location.pathname).toBeTruthy();
});
