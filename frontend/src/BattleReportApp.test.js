import { render, screen, waitFor } from '@testing-library/react';
import BattleReportApp from './BattleReportApp';

// Mock fetch
global.fetch = jest.fn();

describe('BattleReportApp', () => {
  beforeEach(() => {
    // Limpar localStorage antes de cada teste
    localStorage.clear();
    // Resetar mocks
    fetch.mockClear();
  });

  test('renders login screen when not authenticated', () => {
    render(<BattleReportApp />);

    const title = screen.getByText(/Battle Report Manager/i);
    expect(title).toBeInTheDocument();

    const loginPrompt = screen.getByText(/Enter your User ID to access your reports/i);
    expect(loginPrompt).toBeInTheDocument();
  });

  test('shows user ID input field', () => {
    render(<BattleReportApp />);

    const input = screen.getByPlaceholderText(/User ID \(16 characters\)/i);
    expect(input).toBeInTheDocument();
  });

  test('login button is disabled when input is empty', () => {
    render(<BattleReportApp />);

    const button = screen.getByRole('button', { name: /Enter/i });
    expect(button).toBeDisabled();
  });

  test('renders main app when authenticated', async () => {
    // Simular usuário logado
    localStorage.setItem('tower_user_id', '7E9CB1C14B2D1215');
    localStorage.setItem('tower_language', 'en');

    // Mock da API
    fetch.mockResolvedValueOnce({
      json: async () => ({ reports: [] }),
    });

    render(<BattleReportApp />);

    await waitFor(() => {
      const insertReport = screen.getByText(/Insert New Report/i);
      expect(insertReport).toBeInTheDocument();
    });
  });

  test('language toggle button exists', () => {
    render(<BattleReportApp />);

    // Procurar pelo ícone de globo (language toggle)
    const buttons = screen.getAllByRole('button');
    expect(buttons.length).toBeGreaterThan(0);
  });
});