import React from 'react'
import './style.css'
import { PauseOutlined } from '@ant-design/icons'
import { Row, Col, Image } from 'antd';
function IntroBanner() {
  return (
    <div className='banner'>
        <Row>
            <Col span={20}>
                <p className='baner-title'>
                    Medical.AI
                </p>
            </Col>
            <Col span={4}>
                <div className='banner-icon-back'>
                    <PauseOutlined className='baner-icon'/>
                </div>
            </Col>
            <Row span={24} className='banner-image-row'>
                <Image 
                    className='banner-image' 
                    src={"../images/aiBotIcon.svg"}
                    // src={"https://gw.alipayobjects.com/zos/antfincdn/aPkFc8Sj7n/method-draw-image.svg"} 
                    preview={false} 
                />
            </Row>
            <Row span={24} className='w-100'>
                <p className='banner-text-top'>Hey! My name is</p>
            </Row>
            <Row span={24}>
                <p className='banner-name-text'>Medical.AI</p>
            </Row>
            <Row>
                <p className='banner-text'>
                Experience peace of mind and instant access to medical insights anytime, anywhere with Medical.AI.
                </p>
            </Row>
        </Row>

                
    </div>
  ) 
}

export default IntroBanner