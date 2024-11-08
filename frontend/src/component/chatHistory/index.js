import React, { useEffect, useState } from 'react';
import { List, Button } from 'antd';
import { Row, Col } from 'antd';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowRightOutlined, EditOutlined } from '@ant-design/icons';
import './style.css';

function ChatHistory() {
    const [chatHistoryData, setChatHistoryData] = useState([]);
    const chatId = window.location.pathname.split('/')[2];
    const navigate = useNavigate();

    useEffect(() => {
        async function fetchChats() {
            const response = await fetch('http://localhost:8000/chats');
            const data = await response.json();
            // Sort the chat data by last_message_datetime
            const sortedData = data.sort((a, b) => new Date(b.last_message_datetime) - new Date(a.last_message_datetime));
            setChatHistoryData(sortedData);
        }

        fetchChats();
    }, [chatId]);
 

    // Redirect to the default chat page if chatId is not provided
    useEffect(() => {
        if (!chatId) {
            navigate('/'); // Replace '/default-chat-id' with your default chat route
        }
    }, [chatId, navigate]);

    // Function to format date as "Today", "Yesterday", or a date string
    const formatDate = (dateString) => {
        const date = new Date(dateString);
        const today = new Date();
        const yesterday = new Date(today);
        const lastWeek = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);
        lastWeek.setDate(lastWeek.getDate() - 7);

        if (date.toDateString() === today.toDateString()) {
            return 'Today';
        } else if (date.toDateString() === yesterday.toDateString()) {
            return 'Yesterday';
        } else if (date >= lastWeek) {
            return 'Last 7 Days';
        } else {
            return 'Older';
        }
    };

    // Group chat history items by date
    const groupedChatHistory = chatHistoryData.reduce((groups, item) => {
        const dateGroup = formatDate(item.last_message_datetime);
        if (!groups[dateGroup]) {
            groups[dateGroup] = [];
        }
        groups[dateGroup].push(item);
        return groups;
    }, {});

    return (
        <div>
            <div
                id="scrollableDiv"
                className="scrollableDiv"
                style={{
                    height: 500,
                    overflow: 'auto',
                    padding: '0 16px',
                    border: '1px solid rgba(140, 140, 140, 0.35)',
                }}
            >
                <div>

                <Row>
                        <Col span={20}>
                            <p className='list-heading'>New Chat</p>
                        </Col>
                        <Col span={4} style={{"padding-top" : "10px"}}>
                            <Button type="text" className='list-icon-new-chat' onClick={() => navigate('/')}  disabled={window.location.pathname === '/'} >
                                <EditOutlined className='list-icon' />
                                
                            </Button>
                        </Col>
                    </Row>
                    
                
                    <Row>
                        <Col span={24}>
                            <p className='list-heading-history'>Chat History</p>
                        </Col>
                        {/* <Col span={4}>
                            <div className='list-icon-back'>
                                <ArrowRightOutlined className='list-icon' />
                            </div>
                        </Col> */}
                    </Row>
                </div>
                {Object.entries(groupedChatHistory).map(([date, items]) => (
                    <div key={date}>
                        <p className="date-heading">{date}</p>
                        <List
                            dataSource={items}
                            renderItem={(item) => (
                                <List.Item style={{ width: '100%' }} >
                                    <a href={"http://localhost:3000/c/" + item.id} className='chat-item' style={{ width: '100%' }} >
                                        <List.Item.Meta className={chatId === item.id ? 'selected-chat' : ''}
                                            title={item.topic}
                                        />
                                    </a>
                                </List.Item>
                            )}
                        />
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ChatHistory;
