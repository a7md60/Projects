import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Import BrowserRouter and Routes
import IntroBanner from '../../component/introBanner';
import { Row, Col } from 'antd';
import ChatHistory from '../../component/chatHistory';
import Chats from '../../component/chat/index';

import './style.css';

const Home = () => {
  return (
    <Router>
      {" "}
      {/* Wrap your entire application with Router */}
      <div style={{ background: "#0f0f0f" }}>
        <Row>
          <Col className="sider" span={6}>
            <Routes>
              <Route path="/c/:chatId" element={<ChatHistory />} />
              <Route path="/" element={<ChatHistory />} />
            </Routes>
            <IntroBanner />
          </Col>
          <Col span={18}>
            <Routes>
              <Route path="/c/:chatId" element={<Chats />} />
              <Route path="/" element={<Chats />} />
            </Routes>
          </Col>
        </Row>
      </div>
    </Router>
  );
};

export default Home;
