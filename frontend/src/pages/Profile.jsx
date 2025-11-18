import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { toast } from 'react-toastify';

const Profile = () => {
  const { user, updateProfile } = useAuth();
  const [name, setName] = useState(user?.name || '');
  const [interests, setInterests] = useState(
    (user?.research_interests || []).join(', ')
  );
  const [countries, setCountries] = useState(
    (user?.target_countries || []).join(', ')
  );
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const profileData = {
      name,
      research_interests: interests.split(',').map(s => s.trim()).filter(Boolean),
      target_countries: countries.split(',').map(s => s.trim()).filter(Boolean)
    };

    const result = await updateProfile(profileData);
    setLoading(false);

    if (result.success) {
      toast.success('Profile updated successfully!');
    }
  };

  return (
    <div className="px-4 py-6 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Profile</h1>

      <div className="card">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Full Name
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="input"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <input
              type="email"
              value={user?.email || ''}
              className="input bg-gray-100"
              disabled
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Research Interests
              <span className="text-gray-500 text-xs ml-2">(comma separated)</span>
            </label>
            <textarea
              value={interests}
              onChange={(e) => setInterests(e.target.value)}
              className="input"
              rows="3"
              placeholder="e.g., Machine Learning, Deep Learning, Aerospace, Manufacturing"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Target Countries
              <span className="text-gray-500 text-xs ml-2">(comma separated)</span>
            </label>
            <textarea
              value={countries}
              onChange={(e) => setCountries(e.target.value)}
              className="input"
              rows="2"
              placeholder="e.g., USA, UK, Canada, Germany, China"
            />
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary"
            >
              {loading ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Profile;
