import React from 'react';
import { List } from 'antd';
import {Row, Col} from 'antd';
import {ArrowRightOutlined} from '@ant-design/icons'
import './style.css'
function ChatTopics() {
    const data =[
        {
            "name": "Hi",
            "email": "Hi I'm a Medical Assistance Chat Bot, I can help you to book your medical appointment. How can I assist you?",
        },
        {
            "name": "First Date",
            "email": "valeria.blanchard@example.com",
        },
        {
            "name": "Movie Night",
            "email": "gwendolyn.mitchelle@example.com",
        },
        {
            "name": "Home Your",
            "email": "marta.chernenko@example.com",
        },
        {
            "name": "Rist",
            "email": "hasso.rist@example.com",
        },
        {
            "name": "Balderas",
            "email": "marcoantonio.balderas@example.com",
        },
        {
            "name": "Olson",
            "email": "eugene.olson@example.com",
        },
        {
            "name": "Tuominen",
            "email": "aapo.tuominen@example.com",
        }
    ]
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
                  <p className='list-heading'>Scenerio</p> 
                </Col>
                <Col span={4}>
                    <div className='list-icon-back'>
                        <ArrowRightOutlined className='list-icon' />
                    </div>
                </Col>
            </Row>
        </div>

        <List
        dataSource={data}
        renderItem={(item) => (
            <List.Item key={item.email}>
            <List.Item.Meta
                title={<a href="https://ant.design"><p className='text-white' style={{margin:0}}>{item.name}</p></a>}
                description={<p className='text-white'>{item.email}</p>}
            />
            </List.Item>
        )}
        />
        </div>
    </div>
  )
}

export default ChatTopics