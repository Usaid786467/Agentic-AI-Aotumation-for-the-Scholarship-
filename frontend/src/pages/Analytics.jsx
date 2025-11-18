import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Analytics = () => {
  const [stats, setStats] = useState(null);
  const [byCountry, setByCountry] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const [statsRes, countryRes] = await Promise.all([
        api.get('/api/analytics/dashboard'),
        api.get('/api/analytics/by-country')
      ]);
      setStats(statsRes.data);
      setByCountry(countryRes.data.by_country || []);
    } catch (error) {
      console.error('Failed to fetch analytics');
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
      <h1 className="text-3xl font-bold mb-6">Analytics</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <div className="card">
          <h3 className="text-sm font-medium text-gray-600 mb-2">Total Applications</h3>
          <p className="text-4xl font-bold text-primary-600">{stats?.applications?.total || 0}</p>
        </div>
        <div className="card">
          <h3 className="text-sm font-medium text-gray-600 mb-2">Emails Sent</h3>
          <p className="text-4xl font-bold text-green-600">{stats?.emails?.sent || 0}</p>
        </div>
        <div className="card">
          <h3 className="text-sm font-medium text-gray-600 mb-2">Success Rate</h3>
          <p className="text-4xl font-bold text-purple-600">{stats?.success_rate || 0}%</p>
        </div>
      </div>

      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Applications by Country</h2>
        {byCountry.length > 0 ? (
          <div className="space-y-3">
            {byCountry.map((item, idx) => (
              <div key={idx} className="flex items-center justify-between">
                <span className="text-gray-700">{item.country}</span>
                <div className="flex items-center gap-3">
                  <div className="w-48 bg-gray-200 rounded-full h-3">
                    <div
                      className="bg-primary-600 h-3 rounded-full"
                      style={{ width: `${(item.count / byCountry[0].count) * 100}%` }}
                    ></div>
                  </div>
                  <span className="text-gray-900 font-semibold w-8">{item.count}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No data available</p>
        )}
      </div>
    </div>
  );
};

export default Analytics;
