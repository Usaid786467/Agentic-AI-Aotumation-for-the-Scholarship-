import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { toast } from 'react-toastify';

const ProfessorSearch = () => {
  const [professors, setProfessors] = useState([]);
  const [loading, setLoading] = useState(false);
  const [discovering, setDiscovering] = useState(false);

  useEffect(() => {
    fetchProfessors();
  }, []);

  const fetchProfessors = async () => {
    setLoading(true);
    try {
      const response = await api.get('/api/professors/search');
      setProfessors(response.data.professors || []);
    } catch (error) {
      toast.error('Failed to fetch professors');
    } finally {
      setLoading(false);
    }
  };

  const handleDiscover = async () => {
    setDiscovering(true);
    try {
      const response = await api.post('/api/professors/discover');
      toast.success(response.data.message);
      fetchProfessors();
    } catch (error) {
      toast.error('Failed to discover professors');
    } finally {
      setDiscovering(false);
    }
  };

  return (
    <div className="px-4 py-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Professors</h1>
        <button
          onClick={handleDiscover}
          disabled={discovering}
          className="btn btn-primary"
        >
          {discovering ? 'Discovering...' : '🔍 Discover Professors'}
        </button>
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {professors.map((prof) => (
            <div key={prof.id} className="card hover:shadow-lg transition-shadow">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3 className="text-xl font-semibold">{prof.name}</h3>
                  <p className="text-sm text-gray-600">{prof.title}</p>
                </div>
                {prof.match_score && (
                  <span className="bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm font-semibold">
                    {prof.match_score.toFixed(0)}% Match
                  </span>
                )}
              </div>

              {prof.university && (
                <p className="text-sm text-gray-600 mb-2">
                  🎓 {prof.university.name}
                </p>
              )}

              {prof.email && (
                <p className="text-sm text-gray-600 mb-3">
                  📧 {prof.email}
                </p>
              )}

              {prof.research_interests && prof.research_interests.length > 0 && (
                <div className="flex flex-wrap gap-1 mt-3">
                  {prof.research_interests.slice(0, 4).map((interest, idx) => (
                    <span
                      key={idx}
                      className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded"
                    >
                      {interest}
                    </span>
                  ))}
                </div>
              )}

              {prof.h_index && (
                <div className="mt-3 text-sm text-gray-600">
                  <span className="font-medium">H-index:</span> {prof.h_index} |
                  <span className="font-medium ml-2">Citations:</span> {prof.citations}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {!loading && professors.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500">No professors found. Discover universities first, then discover professors!</p>
        </div>
      )}
    </div>
  );
};

export default ProfessorSearch;
