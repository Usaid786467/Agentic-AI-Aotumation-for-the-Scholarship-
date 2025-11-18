import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await api.get('/api/analytics/dashboard');
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="px-4 py-6">
      {/* Welcome Section */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Welcome back, {user?.name}! 👋</h1>
        <p className="mt-2 text-gray-600">Here's your PhD application journey overview</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card bg-gradient-to-br from-blue-500 to-blue-600 text-white">
          <h3 className="text-sm font-medium opacity-90">Total Applications</h3>
          <p className="text-3xl font-bold mt-2">{stats?.applications?.total || 0}</p>
        </div>
        <div className="card bg-gradient-to-br from-green-500 to-green-600 text-white">
          <h3 className="text-sm font-medium opacity-90">Emails Sent</h3>
          <p className="text-3xl font-bold mt-2">{stats?.emails?.sent || 0}</p>
        </div>
        <div className="card bg-gradient-to-br from-purple-500 to-purple-600 text-white">
          <h3 className="text-sm font-medium opacity-90">Responses</h3>
          <p className="text-3xl font-bold mt-2">{stats?.applications?.replied || 0}</p>
        </div>
        <div className="card bg-gradient-to-br from-orange-500 to-orange-600 text-white">
          <h3 className="text-sm font-medium opacity-90">Success Rate</h3>
          <p className="text-3xl font-bold mt-2">{stats?.success_rate || 0}%</p>
        </div>
      </div>

      {/* Opportunities */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Available Opportunities</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Universities</span>
              <span className="text-2xl font-bold text-primary-600">
                {stats?.opportunities?.universities || 0}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Professors</span>
              <span className="text-2xl font-bold text-primary-600">
                {stats?.opportunities?.professors || 0}
              </span>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
          <div className="space-y-2">
            <a href="/universities" className="block btn btn-primary w-full">
              🎓 Discover Universities
            </a>
            <a href="/professors" className="block btn btn-primary w-full">
              👨‍🏫 Find Professors
            </a>
            <a href="/emails" className="block btn btn-secondary w-full">
              📧 Manage Emails
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
