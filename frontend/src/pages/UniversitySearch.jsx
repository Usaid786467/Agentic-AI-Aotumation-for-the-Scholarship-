import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { toast } from 'react-toastify';

const UniversitySearch = () => {
  const [universities, setUniversities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [discovering, setDiscovering] = useState(false);

  useEffect(() => {
    fetchUniversities();
  }, []);

  const fetchUniversities = async () => {
    setLoading(true);
    try {
      const response = await api.get('/api/universities/search');
      setUniversities(response.data.universities || []);
    } catch (error) {
      toast.error('Failed to fetch universities');
    } finally {
      setLoading(false);
    }
  };

  const handleDiscover = async () => {
    setDiscovering(true);
    try {
      const response = await api.post('/api/universities/discover');
      toast.success(response.data.message);
      fetchUniversities();
    } catch (error) {
      toast.error('Failed to discover universities');
    } finally {
      setDiscovering(false);
    }
  };

  return (
    <div className="px-4 py-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Universities</h1>
        <button
          onClick={handleDiscover}
          disabled={discovering}
          className="btn btn-primary"
        >
          {discovering ? 'Discovering...' : '🔍 Discover Universities'}
        </button>
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {universities.map((uni) => (
            <div key={uni.id} className="card hover:shadow-lg transition-shadow">
              <div className="flex justify-between items-start mb-2">
                <h3 className="text-lg font-semibold">{uni.name}</h3>
                {uni.has_scholarship && (
                  <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                    💰 Funded
                  </span>
                )}
              </div>
              <p className="text-gray-600 text-sm mb-2">📍 {uni.country}</p>
              {uni.research_areas && uni.research_areas.length > 0 && (
                <div className="flex flex-wrap gap-1 mt-3">
                  {uni.research_areas.slice(0, 3).map((area, idx) => (
                    <span key={idx} className="bg-primary-100 text-primary-700 text-xs px-2 py-1 rounded">
                      {area}
                    </span>
                  ))}
                </div>
              )}
              <a
                href={uni.website}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-3 text-primary-600 hover:text-primary-700 text-sm font-medium"
              >
                Visit Website →
              </a>
            </div>
          ))}
        </div>
      )}

      {!loading && universities.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500">No universities found. Click "Discover Universities" to get started!</p>
        </div>
      )}
    </div>
  );
};

export default UniversitySearch;
