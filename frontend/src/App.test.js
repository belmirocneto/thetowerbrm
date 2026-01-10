import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Battle Report Manager', () => {
  render(<App />);
  const titleElement = screen.getByText(/Battle Report Manager/i);
  expect(titleElement).toBeInTheDocument();
});

test('renders login screen when not authenticated', () => {
  render(<App />);
  const loginText = screen.getByText(/Enter your User ID to access your reports/i);
  expect(loginText).toBeInTheDocument();
});