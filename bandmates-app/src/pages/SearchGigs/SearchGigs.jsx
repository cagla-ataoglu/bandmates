import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../../components/Navbar/Navbar';
import GigsFeed from '../../components/GigsFeed/GigsFeed';
import GigsBar from '../../components/GigsBar/GigsBar';
import SearchGigsBar from '../../components/SearchGigsBar/SearchGigsBar';
import MiniProfileCard from '../../components/MiniProfileCard/MiniProfileCard';
import './SearchGigs.css';

const SearchGigs = () => {
  const navigate = useNavigate();
  const [filters, setFilters] = useState({
    gigName: '',
    dateFrom: '',
    dateTo: '',
    instrument: ''
  });
  const [posts, setPosts] = useState([]);
  const [allPosts, setAllPosts] = useState([]);

  useEffect(() => {
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      navigate('/login');
    }
  }, [navigate]);

  useEffect(() => {
    fetchPosts();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [filters, allPosts]);

  const fetchPosts = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_GIG_API}/get_gig_postings`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      const data = await response.json();
      if (response.ok) {
        if (data.status === 'success') {
          const sortedPosts = data.posts.sort((a, b) => new Date(b.Timestamp) - new Date(a.Timestamp));
          setAllPosts(sortedPosts);
          setPosts(sortedPosts);
        } else {
          console.error('Failed to fetch posts:', data.message);
        }
      }
      
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
  };

  const applyFilters = () => {
    fetchPosts().then(() => {
      const filteredPosts = allPosts.filter(post => {
        const postDate = new Date(post.GigDate);
        const fromDate = filters.dateFrom ? new Date(filters.dateFrom) : null;
        const toDate = filters.dateTo ? new Date(filters.dateTo) : null;
        const dateMatch = (!fromDate || postDate >= fromDate) && (!toDate || postDate <= toDate);

        const nameMatch = !filters.gigName || post.GigName.toLowerCase().includes(filters.gigName.toLowerCase());
        const instrumentMatch = !filters.instrument || post.LookingFor.toLowerCase().includes(filters.instrument.toLowerCase());

        return nameMatch && instrumentMatch && dateMatch;
      });
      setPosts(filteredPosts);
    });
  };

  const handlePostClick = () => {
    navigate('/post_gig');
  };

  const handleFilterChange= (newFilters) => {
    setFilters(newFilters);
  }

  return (
    <>
      <Navbar />
      <div className="gigs-container">
        <div className="gigs-content-container">
          <MiniProfileCard username={localStorage.getItem('username')}/>
          <GigsBar />
          <button className="gigs-container button" onClick={handlePostClick}>
            Post a Gig
          </button>
        </div>
        <div className="gigs-content-container">
          <div className="gigs-vertical-content">
            <GigsFeed posts={posts}/>
          </div>
        </div>
        <div className="gigs-content-container" >
          <SearchGigsBar onFilterChange={handleFilterChange} />
        </div>
      </div>
    </>
  );
}

export default SearchGigs;
