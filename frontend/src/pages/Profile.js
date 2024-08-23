import React, { useState, useEffect } from 'react';
import { fetchUrlInfo as fetchUserInfo } from '../services/userService';

const Profile = () => {
  const [userInfo, setUserInfo] = useState(null);

  useEffect(() => {
    const getUserInfo = async () => {
      const data = await fetchUserInfo('testuser');
      setUserInfo(data);
    };
    getUserInfo();
  }, []);

  return (
    <div>
      <h2>Profile Page</h2>
      {userInfo ? (
        <div>
          <p>Username: {userInfo.username}</p>
          <p>Full Name: {userInfo.full_name}</p>
          <p>Email: {userInfo.email}</p>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Profile;
