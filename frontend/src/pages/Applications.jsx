import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Applications = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    setLoading(true);
    try {
      const response = await api.get('/api/applications/');
      setApplications(response.data.applications || []);
    } catch (error) {
      console.error('Failed to fetch applications');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      draft: 'bg-gray-100 text-gray-700',
      sent: 'bg-blue-100 text-blue-700',
      delivered: 'bg-indigo-100 text-indigo-700',
      opened: 'bg-purple-100 text-purple-700',
      replied: 'bg-green-100 text-green-700',
      rejected: 'bg-red-100 text-red-700'
    };
    return colors[status] || 'bg-gray-100 text-gray-700';
  };

  return (
    <div className="px-4 py-6">
      <h1 className="text-3xl font-bold mb-6">Applications</h1>

      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : applications.length > 0 ? (
        <div className="grid grid-cols-1 gap-4">
          {applications.map((app) => (
            <div key={app.id} className="card hover:shadow-lg transition-shadow">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold mb-1">
                    {app.professor?.name || 'Professor'}
                  </h3>
                  <p className="text-gray-600 text-sm">
                    {app.university?.name || 'University'} • {app.university?.country || ''}
                  </p>
                  {app.match_score && (
                    <p className="text-sm text-primary-600 mt-2">
                      Match Score: {app.match_score.toFixed(0)}%
                    </p>
                  )}
                  {app.notes && (
                    <p className="text-sm text-gray-600 mt-2">{app.notes}</p>
                  )}
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(app.status)}`}>
                  {app.status}
                </span>
              </div>
              <div className="mt-4 text-xs text-gray-500">
                Created: {new Date(app.created_at).toLocaleDateString()}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-500">No applications yet. Start by discovering universities and professors!</p>
        </div>
      )}
    </div>
  );
};

export default Applications;
