import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { toast } from 'react-toastify';

const EmailManagement = () => {
  const [emails, setEmails] = useState([]);
  const [batches, setBatches] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchEmails();
    fetchBatches();
  }, []);

  const fetchEmails = async () => {
    setLoading(true);
    try {
      const response = await api.get('/api/emails/');
      setEmails(response.data.emails || []);
    } catch (error) {
      console.error('Failed to fetch emails');
    } finally {
      setLoading(false);
    }
  };

  const fetchBatches = async () => {
    try {
      const response = await api.get('/api/emails/batches');
      setBatches(response.data.batches || []);
    } catch (error) {
      console.error('Failed to fetch batches');
    }
  };

  return (
    <div className="px-4 py-6">
      <h1 className="text-3xl font-bold mb-6">Email Management</h1>

      {/* Batches */}
      <div className="card mb-6">
        <h2 className="text-xl font-semibold mb-4">Email Batches</h2>
        {batches.length > 0 ? (
          <div className="space-y-3">
            {batches.map((batch) => (
              <div key={batch.id} className="border rounded-lg p-4 hover:bg-gray-50">
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className="font-medium">{batch.name}</h3>
                    <p className="text-sm text-gray-600 mt-1">
                      Total: {batch.total_count} | Sent: {batch.sent_count} | Status: {batch.status}
                    </p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm ${
                    batch.status === 'completed' ? 'bg-green-100 text-green-700' :
                    batch.status === 'approved' ? 'bg-blue-100 text-blue-700' :
                    'bg-gray-100 text-gray-700'
                  }`}>
                    {batch.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No email batches yet</p>
        )}
      </div>

      {/* Emails */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Recent Emails</h2>
        {loading ? (
          <div className="flex justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          </div>
        ) : emails.length > 0 ? (
          <div className="space-y-4">
            {emails.map((email) => (
              <div key={email.id} className="border rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-medium">{email.subject}</h3>
                  <span className={`px-2 py-1 rounded text-xs ${
                    email.status === 'sent' ? 'bg-green-100 text-green-700' :
                    email.status === 'failed' ? 'bg-red-100 text-red-700' :
                    'bg-yellow-100 text-yellow-700'
                  }`}>
                    {email.status}
                  </span>
                </div>
                <p className="text-sm text-gray-600 line-clamp-2">{email.body.substring(0, 150)}...</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No emails yet. Generate emails from your applications!</p>
        )}
      </div>
    </div>
  );
};

export default EmailManagement;
