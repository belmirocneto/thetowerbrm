import React, { useState, useEffect } from 'react';
import { ComposedChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Upload, Database, TrendingUp, LogOut, Trash2, Globe } from 'lucide-react';
import { API_CONFIG } from './config';

const API_URL = API_CONFIG.BASE_URL;

// Traduções
const translations = {
  en: {
    title: 'Battle Report Manager',
    insertUserId: 'Enter your User ID to access your reports',
    userId: 'User ID',
    characters: 'characters',
    enter: 'Enter',
    logout: 'Logout',
    insertNewReport: 'Insert New Report',
    pasteReport: 'Paste the complete Battle Report content here...',
    sendReport: 'Send Report',
    processing: 'Processing...',
    reportSaved: '✓ Report saved successfully!',
    lastReports: 'Latest Reports',
    display: 'Display',
    noReports: 'No reports found',
    backToPage: 'Back to Page',
    battleDate: 'Battle Date',
    tier: 'Tier',
    wave: 'Wave',
    realTime: 'Real Time',
    runsPerDay: 'Runs/Day',
    coinsEarned: 'Coins Earned',
    coinsPerDay: 'Coins/Day',
    cellsEarned: 'Cells Earned',
    cellsPerDay: 'Cells/Day',
    rerollShards: 'Reroll Shards',
    rerollsPerDay: 'Rerolls/Day',
    actions: 'Actions',
    highlightBest: 'Highlight best',
    previous: 'Previous',
    next: 'Next',
    page: 'Page',
    statistics: 'Statistics',
    confirmDelete: 'Confirm Deletion',
    confirmDeleteMsg: 'Are you sure you want to delete this report? This action cannot be undone.',
    delete: 'Delete',
    cancel: 'Cancel',
  },
  pt: {
    title: 'Gerenciador de Relatórios',
    insertUserId: 'Insira seu User ID para acessar seus reports',
    userId: 'User ID',
    characters: 'caracteres',
    enter: 'Entrar',
    logout: 'Sair',
    insertNewReport: 'Inserir Novo Report',
    pasteReport: 'Cole aqui o conteúdo completo do Battle Report...',
    sendReport: 'Enviar Report',
    processing: 'Processando...',
    reportSaved: '✓ Report salvo com sucesso!',
    lastReports: 'Últimos Reports',
    display: 'Exibir',
    noReports: 'Nenhum report encontrado',
    backToPage: 'Voltar para Página',
    battleDate: 'Data da Batalha',
    tier: 'Grau',
    wave: 'Onda',
    realTime: 'Tempo Real',
    runsPerDay: 'Runs/Dia',
    coinsEarned: 'Moedas Ganhas',
    coinsPerDay: 'Moedas/Dia',
    cellsEarned: 'Células Ganhas',
    cellsPerDay: 'Células/Dia',
    rerollShards: 'Fragmentos de Variação',
    rerollsPerDay: 'Rerolls/Dia',
    actions: 'Ações',
    highlightBest: 'Destacar melhor',
    previous: 'Anterior',
    next: 'Próxima',
    page: 'Página',
    statistics: 'Estatísticas',
    confirmDelete: 'Confirmar Exclusão',
    confirmDeleteMsg: 'Tem certeza que deseja deletar este report? Esta ação não pode ser desfeita.',
    delete: 'Deletar',
    cancel: 'Cancelar',
  }
};

export default function BattleReportApp() {
  const [language, setLanguage] = useState('en');
  const [userId, setUserId] = useState('');
  const [userIdInput, setUserIdInput] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [rawData, setRawData] = useState('');
  const [reports, setReports] = useState([]);
  const [limit, setLimit] = useState(15);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [highlightMode, setHighlightMode] = useState('coins');
  const [deleteConfirm, setDeleteConfirm] = useState(null);

  const t = translations[language];

  useEffect(() => {
    const browserLang = navigator.language || navigator.userLanguage;
    const detectedLang = browserLang.startsWith('pt') ? 'pt' : 'en';
    const savedLang = localStorage.getItem('tower_language') || detectedLang;
    setLanguage(savedLang);

    const savedUserId = localStorage.getItem('tower_user_id');
    if (savedUserId && savedUserId.length === 16) {
      setUserId(savedUserId);
      setIsLoggedIn(true);
    }
  }, []);

  useEffect(() => {
    if (isLoggedIn && userId) {
      fetchReports();
    }
  }, [limit, page, isLoggedIn, userId]);

  const changeLanguage = (lang) => {
    setLanguage(lang);
    localStorage.setItem('tower_language', lang);
  };

  const handleLogin = () => {
    const trimmedId = userIdInput.trim();
    if (trimmedId.length === 16) {
      localStorage.setItem('tower_user_id', trimmedId);
      setUserId(trimmedId);
      setIsLoggedIn(true);
    } else {
      alert(`${t.userId} must be exactly 16 characters. You entered ${trimmedId.length} characters.`);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('tower_user_id');
    setUserId('');
    setUserIdInput('');
    setIsLoggedIn(false);
    setReports([]);
  };

  const fetchReports = async () => {
    try {
      const response = await fetch(
        `${API_URL}/reports?user_id=${userId}&limit=${limit}&page=${page}`, {
          method: 'GET',
          headers: {
            'x-api-key': API_CONFIG.API_KEY
          }
        }
      );
      const data = await response.json();
      setReports(data.reports || []);
    } catch (error) {
      console.error('Error fetching reports:', error);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    setMessage('');

    try {
      const response = await fetch(`${API_URL}/reports`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ raw_data: rawData, user_id: userId }),
      });

      const data = await response.json();
      
      if (response.ok) {
        setMessage(t.reportSaved);
        setRawData('');
        fetchReports();
      } else {
        setMessage(`✗ Error: ${data.error}`);
      }
    } catch (error) {
      setMessage('✗ Error connecting to server');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (reportId) => {
    try {
      const response = await fetch(`${API_URL}/reports/${reportId}?user_id=${userId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setMessage('✓ Report deleted successfully!');
        fetchReports();
      } else {
        setMessage('✗ Error deleting report');
      }
    } catch (error) {
      setMessage('✗ Error connecting to server');
    } finally {
      setDeleteConfirm(null);
    }
  };

  const parseRealTime = (timeStr) => {
    if (!timeStr) return 0;
    const match = timeStr.match(/(\d+)h\s*(\d+)m/);
    if (match) {
      const hours = parseInt(match[1]);
      const minutes = parseInt(match[2]);
      return hours + minutes / 60;
    }
    return 0;
  };

  const calculateRunsPerDay = (realTime) => {
    const hoursPerRun = parseRealTime(realTime);
    if (hoursPerRun === 0) return 0;
    return 24 / hoursPerRun;
  };

  const enrichedReports = reports.map(report => {
    const runsPerDay = calculateRunsPerDay(report.real_time);
    return {
      ...report,
      runs_per_day: runsPerDay,
      coins_per_day: (report.coins_earned || 0) * runsPerDay,
      cells_per_day: (report.cells_earned || 0) * runsPerDay,
      rerolls_per_day: (report.reroll_shards_earned || 0) * runsPerDay,
    };
  });

  const getMaxPerDay = (field) => {
    if (enrichedReports.length === 0) return 0;
    return Math.max(...enrichedReports.map(r => r[field] || 0));
  };

  const maxCoinsPerDay = getMaxPerDay('coins_per_day');
  const maxCellsPerDay = getMaxPerDay('cells_per_day');
  const maxRerollsPerDay = getMaxPerDay('rerolls_per_day');

  const shouldHighlight = (report) => {
    switch (highlightMode) {
      case 'coins':
        return report.coins_per_day === maxCoinsPerDay && maxCoinsPerDay > 0;
      case 'cells':
        return report.cells_per_day === maxCellsPerDay && maxCellsPerDay > 0;
      case 'rerolls':
        return report.rerolls_per_day === maxRerollsPerDay && maxRerollsPerDay > 0;
      default:
        return false;
    }
  };

  const formatNumber = (num) => {
    if (num === null || num === undefined || num === 0) return '0';
    
    const number = typeof num === 'string' ? parseFloat(num.replace(/,/g, '')) : Number(num);
    
    if (isNaN(number)) return '0';
    
    const suffixes = [
      [1e30, 'N'],
      [1e27, 'D'],
      [1e24, 'S'],
      [1e21, 's'],
      [1e18, 'Q'],
      [1e15, 'q'],
      [1e12, 'T'],
      [1e9, 'B'],
      [1e6, 'M'],
      [1e3, 'K']
    ];
    
    for (const [threshold, suffix] of suffixes) {
      if (Math.abs(number) >= threshold) {
        const value = number / threshold;
        return `${value.toFixed(2)}${suffix}`;
      }
    }
    
    if (number >= 100) return number.toFixed(0);
    if (number >= 10) return number.toFixed(1);
    return number.toFixed(2);
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleString(language === 'pt' ? 'pt-BR' : 'en-US');
  };

  const formatAxisNumber = (value) => {
    return formatNumber(value);
  };

  const chartData = reports.map(r => {
    const date = new Date(r.battle_date);
    const dateLabel = `${date.toLocaleDateString(language === 'pt' ? 'pt-BR' : 'en-US', { day: '2-digit', month: '2-digit' })} ${date.getHours()}h${String(date.getMinutes()).padStart(2, '0')}`;
    
    return {
      dateLabel,
      timestamp: date.getTime(),
      tier: r.tier,
      coins: r.coins_earned || 0,
      cells: r.cells_earned || 0,
      shards: r.reroll_shards_earned || 0,
    };
  }).reverse();

  const uniqueTiers = [...new Set(reports.map(r => r.tier))].sort((a, b) => a - b);

  const tierColors = {
    1: '#ef4444', 2: '#f97316', 3: '#f59e0b', 4: '#eab308', 5: '#84cc16',
    6: '#22c55e', 7: '#10b981', 8: '#14b8a6', 9: '#06b6d4', 10: '#0ea5e9',
    11: '#3b82f6', 12: '#6366f1', 13: '#8b5cf6', 14: '#a855f7', 15: '#c026d3',
    16: '#d946ef', 17: '#ec4899', 18: '#f43f5e', 19: '#fb7185', 20: '#fdba74',
    21: '#fcd34d', 22: '#bef264', 23: '#86efac', 24: '#67e8f9', 25: '#a5b4fc',
  };

  const getTierColor = (tier) => {
    if (tierColors[tier]) return tierColors[tier];
    const hue = (tier * 137.5) % 360;
    return `hsl(${hue}, 70%, 60%)`;
  };

  const CustomDot = (props) => {
    const { cx, cy, payload } = props;
    const color = getTierColor(payload.tier);
    const radius = window.innerWidth < 768 ? 3 : 5;
    
    return (
      <circle
        cx={cx}
        cy={cy}
        r={radius}
        fill={color}
        stroke={color}
        strokeWidth={window.innerWidth < 768 ? 1 : 2}
      />
    );
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length > 0) {
      const data = payload[0].payload;
      
      return (
        <div className="bg-slate-900 border border-slate-600 p-3 rounded shadow-lg">
          <p className="text-slate-300 font-semibold mb-2">{label}</p>
          <p className="text-purple-400 text-sm">{t.tier}: {data.tier}</p>
          <p className="text-blue-400 text-sm">{t.coinsEarned}: {formatNumber(data.coins)}</p>
          <p className="text-green-400 text-sm">{t.cellsEarned}: {formatNumber(data.cells)}</p>
          <p className="text-orange-400 text-sm">{t.rerollShards}: {formatNumber(data.shards)}</p>
        </div>
      );
    }
    return null;
  };

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white flex items-center justify-center p-6">
        <div className="bg-slate-800 rounded-lg shadow-2xl p-8 max-w-md w-full border border-slate-700">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <Database className="w-10 h-10 text-blue-400" />
              <h1 className="text-2xl font-bold">{t.title}</h1>
            </div>
            <button
              onClick={() => changeLanguage(language === 'en' ? 'pt' : 'en')}
              className="p-2 hover:bg-slate-700 rounded transition-colors"
              title={language === 'en' ? 'Português' : 'English'}
            >
              <Globe className="w-5 h-5" />
            </button>
          </div>
          
          <p className="text-slate-400 mb-6">{t.insertUserId}</p>
          
          <input
            type="text"
            value={userIdInput}
            onChange={(e) => setUserIdInput(e.target.value.toUpperCase().trim())}
            placeholder={`${t.userId} (16 ${t.characters})`}
            maxLength={16}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white font-mono focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
            onKeyPress={(e) => {
              if (e.key === 'Enter' && userIdInput.trim().length === 16) {
                handleLogin();
              }
            }}
          />
          
          <p className={`text-sm mb-4 ${userIdInput.trim().length === 16 ? 'text-green-400' : 'text-slate-500'}`}>
            {userIdInput.trim().length}/16 {t.characters}
          </p>
          
          <button
            onClick={handleLogin}
            disabled={userIdInput.trim().length !== 16}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 disabled:cursor-not-allowed px-6 py-3 rounded-lg font-semibold transition-colors"
          >
            {t.enter}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white p-6">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8 flex items-center justify-between flex-wrap gap-4">
          <div>
            <h1 className="text-4xl font-bold mb-2 flex items-center gap-3">
              <Database className="w-10 h-10 text-blue-400" />
              {t.title}
            </h1>
            <p className="text-slate-400">{t.userId}: <span className="font-mono text-blue-400">{userId}</span></p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => changeLanguage(language === 'en' ? 'pt' : 'en')}
              className="flex items-center gap-2 bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded-lg transition-colors"
              title={language === 'en' ? 'Português' : 'English'}
            >
              <Globe className="w-4 h-4" />
              {language === 'en' ? 'PT' : 'EN'}
            </button>
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg transition-colors"
            >
              <LogOut className="w-4 h-4" />
              {t.logout}
            </button>
          </div>
        </header>

        <div className="bg-slate-800 rounded-lg shadow-xl p-6 mb-8 border border-slate-700">
          <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
            <Upload className="w-6 h-6 text-green-400" />
            {t.insertNewReport}
          </h2>
          <div>
            <textarea
              value={rawData}
              onChange={(e) => setRawData(e.target.value)}
              placeholder={t.pasteReport}
              className="w-full h-64 bg-slate-900 border border-slate-700 rounded-lg p-4 font-mono text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={loading}
            />
            <div className="mt-4 flex items-center justify-between">
              <button
                onClick={handleSubmit}
                disabled={loading || !rawData.trim()}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 disabled:cursor-not-allowed px-6 py-2 rounded-lg font-semibold transition-colors"
              >
                {loading ? t.processing : t.sendReport}
              </button>
              {message && (
                <span className={`text-sm ${message.startsWith('✓') ? 'text-green-400' : 'text-red-400'}`}>
                  {message}
                </span>
              )}
            </div>
          </div>
        </div>

        {deleteConfirm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-slate-800 rounded-lg p-6 max-w-md w-full border border-slate-700">
              <h3 className="text-xl font-semibold mb-4">{t.confirmDelete}</h3>
              <p className="text-slate-400 mb-6">{t.confirmDeleteMsg}</p>
              <div className="flex gap-3">
                <button
                  onClick={() => handleDelete(deleteConfirm)}
                  className="flex-1 bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg transition-colors"
                >
                  {t.delete}
                </button>
                <button
                  onClick={() => setDeleteConfirm(null)}
                  className="flex-1 bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded-lg transition-colors"
                >
                  {t.cancel}
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="bg-slate-800 rounded-lg shadow-xl p-6 mb-8 border border-slate-700">
          <div className="flex items-center justify-between mb-4 flex-wrap gap-4">
            <h2 className="text-2xl font-semibold">{t.lastReports}</h2>
            <div className="flex items-center gap-4">
              <label className="flex items-center gap-2 text-sm">
                {t.display}:
                <select
                  value={limit}
                  onChange={(e) => setLimit(Number(e.target.value))}
                  className="bg-slate-700 border border-slate-600 rounded px-3 py-1 text-white"
                >
                  <option value={5}>5</option>
                  <option value={10}>10</option>
                  <option value={15}>15</option>
                  <option value={20}>20</option>
                </select>
              </label>
            </div>
          </div>

          {enrichedReports.length === 0 ? (
            <div>
              <p className="text-slate-400 text-center py-8">{t.noReports}</p>
              {page > 1 && (
                <div className="flex items-center justify-center mt-4">
                  <button
                    onClick={() => setPage(Math.max(1, page - 1))}
                    className="bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded transition-colors border border-slate-600"
                  >
                    {t.backToPage} {page - 1}
                  </button>
                </div>
              )}
            </div>
          ) : (
            <>
              <div className="overflow-x-auto">
                <table className="w-full text-sm border-collapse">
                  <thead>
                    <tr className="bg-slate-700">
                      <th className="text-left py-3 px-4 font-semibold border border-slate-600">{t.battleDate}</th>
                      <th className="text-right py-3 px-4 font-semibold border border-slate-600">{t.tier}</th>
                      <th className="text-right py-3 px-4 font-semibold border border-slate-600">{t.wave}</th>
                      <th className="text-right py-3 px-4 font-semibold border border-slate-600">{t.realTime}</th>
                      <th className="text-right py-3 px-4 font-semibold border border-slate-600">{t.runsPerDay}</th>
                      <th className="text-right py-3 px-4 font-semibold border border-slate-600">{t.coinsEarned}</th>
                      <th className="text-right py-3 px-4 font-semibold border border-slate-600">{t.coinsPerDay}</th>
                      <th className="text-right py-3 px-4 font-semibold border border-slate-600">{t.cellsEarned}</th>
                      <th className="text-right py-3 px-4 font-semibold border border-slate-600">{t.cellsPerDay}</th>
                      <th className="text-right py-3 px-4 font-semibold border border-slate-600">{t.rerollShards}</th>
                      <th className="text-right py-3 px-4 font-semibold border border-slate-600">{t.rerollsPerDay}</th>
                      <th className="text-center py-3 px-4 font-semibold border border-slate-600">{t.actions}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {enrichedReports.map((report, index) => {
                      const isHighlighted = shouldHighlight(report);
                      return (
                        <tr 
                          key={report.id} 
                          className={`${isHighlighted ? 'bg-yellow-900 bg-opacity-40' : index % 2 === 0 ? 'bg-slate-800' : 'bg-slate-750'} hover:bg-slate-700 transition-colors`}
                        >
                          <td className="py-3 px-4 border border-slate-600">{formatDate(report.battle_date)}</td>
                          <td className="text-right py-3 px-4 border border-slate-600">{report.tier}</td>
                          <td className="text-right py-3 px-4 border border-slate-600">{report.wave}</td>
                          <td className="text-right py-3 px-4 border border-slate-600">{report.real_time}</td>
                          <td className="text-right py-3 px-4 border border-slate-600 text-purple-400 font-semibold">{report.runs_per_day.toFixed(2)}</td>
                          <td className="text-right py-3 px-4 text-blue-400 border border-slate-600 font-semibold">{formatNumber(report.coins_earned)}</td>
                          <td className="text-right py-3 px-4 text-blue-300 border border-slate-600 font-semibold">{formatNumber(report.coins_per_day)}</td>
                          <td className="text-right py-3 px-4 text-green-400 border border-slate-600 font-semibold">{formatNumber(report.cells_earned)}</td>
                          <td className="text-right py-3 px-4 text-green-300 border border-slate-600 font-semibold">{formatNumber(report.cells_per_day)}</td>
                          <td className="text-right py-3 px-4 text-orange-400 border border-slate-600 font-semibold">{formatNumber(report.reroll_shards_earned)}</td>
                          <td className="text-right py-3 px-4 text-orange-300 border border-slate-600 font-semibold">{formatNumber(report.rerolls_per_day)}</td>
                          <td className="text-center py-3 px-4 border border-slate-600">
                            <button
                              onClick={() => setDeleteConfirm(report.id)}
                              className="text-red-400 hover:text-red-300 transition-colors"
                              title={t.delete}
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              <div className="mt-6 flex items-center justify-center gap-6 flex-wrap">
                <div className="flex items-center gap-4">
                  <span className="text-sm text-slate-400">{t.highlightBest}:</span>
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      name="highlight"
                      value="coins"
                      checked={highlightMode === 'coins'}
                      onChange={(e) => setHighlightMode(e.target.value)}
                    />
                    <span className="text-sm">{t.coinsPerDay}</span>
                  </label>
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      name="highlight"
                      value="cells"
                      checked={highlightMode === 'cells'}
                      onChange={(e) => setHighlightMode(e.target.value)}
                    />
                    <span className="text-sm">{t.cellsPerDay}</span>
                  </label>
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      name="highlight"
                      value="rerolls"
                      checked={highlightMode === 'rerolls'}
                      onChange={(e) => setHighlightMode(e.target.value)}
                    />
                    <span className="text-sm">{t.rerollsPerDay}</span>
                  </label>
                </div>
              </div>

              <div className="flex items-center justify-between mt-4">
                <button
                  onClick={() => setPage(Math.max(1, page - 1))}
                  disabled={page === 1}
                  className="bg-slate-700 hover:bg-slate-600 disabled:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50 px-4 py-2 rounded transition-colors border border-slate-600"
                >
                  {t.previous}
                </button>
                <span className="text-sm text-slate-400">{t.page} {page}</span>
                <button
                  onClick={() => setPage(page + 1)}
                  disabled={enrichedReports.length < limit}
                  className="bg-slate-700 hover:bg-slate-600 disabled:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50 px-4 py-2 rounded transition-colors border border-slate-600"
                >
                  {t.next}
                </button>
              </div>
            </>
          )}
        </div>

        {reports.length > 0 && (
          <div className="bg-slate-800 rounded-lg shadow-xl p-6 border border-slate-700">
            <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2">
              <TrendingUp className="w-6 h-6 text-purple-400" />
              {t.statistics}
            </h2>
            
            <div className="space-y-8">
              <div>
                <h3 className="text-lg font-medium mb-3 text-slate-300">{t.coinsEarned}</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <ComposedChart 
                    data={chartData}
                    syncId="battleCharts"
                    margin={{ top: 5, right: 20, left: 60, bottom: 80 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis 
                      dataKey="dateLabel" 
                      stroke="#9CA3AF" 
                      angle={-45}
                      textAnchor="end"
                      height={80}
                      tick={{ fontSize: 11 }}
                    />
                    <YAxis 
                      stroke="#9CA3AF" 
                      tickFormatter={formatAxisNumber}
                      width={80}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend 
                      wrapperStyle={{ paddingTop: '20px' }}
                      payload={uniqueTiers.map(tier => ({
                        value: `${t.tier} ${tier}`,
                        type: 'circle',
                        color: getTierColor(tier)
                      }))}
                    />
                    <Line
                      type="monotone"
                      dataKey="coins"
                      stroke="#60a5fa"
                      strokeWidth={2}
                      dot={<CustomDot />}
                      name={t.coinsEarned}
                    />
                  </ComposedChart>
                </ResponsiveContainer>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-medium mb-3 text-slate-300">{t.cellsEarned}</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <ComposedChart 
                      data={chartData}
                      syncId="battleCharts"
                      margin={{ top: 5, right: 20, left: 60, bottom: 80 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                      <XAxis 
                        dataKey="dateLabel" 
                        stroke="#9CA3AF"
                        angle={-45}
                        textAnchor="end"
                        height={80}
                        tick={{ fontSize: 11 }}
                      />
                      <YAxis 
                        stroke="#9CA3AF" 
                        tickFormatter={formatAxisNumber}
                        width={80}
                      />
                      <Tooltip content={<CustomTooltip />} />
                      <Legend 
                        wrapperStyle={{ paddingTop: '20px' }}
                        payload={uniqueTiers.map(tier => ({
                          value: `${t.tier} ${tier}`,
                          type: 'circle',
                          color: getTierColor(tier)
                        }))}
                      />
                      <Line
                        type="monotone"
                        dataKey="cells"
                        stroke="#4ade80"
                        strokeWidth={2}
                        dot={<CustomDot />}
                        name={t.cellsEarned}
                      />
                    </ComposedChart>
                  </ResponsiveContainer>
                </div>

                <div>
                  <h3 className="text-lg font-medium mb-3 text-slate-300">{t.rerollShards}</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <ComposedChart 
                      data={chartData}
                      syncId="battleCharts"
                      margin={{ top: 5, right: 20, left: 60, bottom: 80 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                      <XAxis 
                        dataKey="dateLabel" 
                        stroke="#9CA3AF"
                        angle={-45}
                        textAnchor="end"
                        height={80}
                        tick={{ fontSize: 11 }}
                      />
                      <YAxis 
                        stroke="#9CA3AF" 
                        tickFormatter={formatAxisNumber}
                        width={80}
                      />
                      <Tooltip content={<CustomTooltip />} />
                      <Legend 
                        wrapperStyle={{ paddingTop: '20px' }}
                        payload={uniqueTiers.map(tier => ({
                          value: `${t.tier} ${tier}`,
                          type: 'circle',
                          color: getTierColor(tier)
                        }))}
                      />
                      <Line
                        type="monotone"
                        dataKey="shards"
                        stroke="#fb923c"
                        strokeWidth={2}
                        dot={<CustomDot />}
                        name={t.rerollShards}
                      />
                    </ComposedChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}