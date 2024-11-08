import React, { useState, useEffect, useRef, useCallback } from "react";
import { Row, Col } from "antd";
import axios from "axios";
import uuid from "react-uuid";
import RecordIcon from "./RecordIcon";

import { useParams } from "react-router-dom";

import "./style.scss";
import { formatChats } from "../helper";
import { useNavigate } from 'react-router-dom';

import { DislikeOutlined } from '@ant-design/icons';

function Chats() {
  const { chatId } = useParams();
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loader, setLoader] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState("English"); // Default language
  const [showReportPopup, setShowReportPopup] = useState(false);
  const [reportDescription, setReportDescription] = useState("");
  const [selectedmessage_id, setSelectedmessage_id] = useState(null);
  const chatContainerRef = useRef();
  const lastMessageRef = useRef();
  const navigate = useNavigate();

  useEffect(() => {
    // Scroll to the bottom of the window when chatHistory changes
    chatContainerRef.current.scrollTo({
      top: chatContainerRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [chatHistory]);

  useEffect(() => {
    const fetchChatHistory = async () => {
      try {
        // Fetch chat history based on chatId if it exists
        if (chatId) {
          const response = await axios.get(
            `http://127.0.0.1:8000/chat/${chatId}`
          );
          const { data } = response;
          setChatHistory(data);
          console.log(data);
        } else {
          setChatHistory([]);
        }
      } catch (error) {
        console.error("Error fetching chat history:", error);
      }
    };

    fetchChatHistory();
  }, [chatId]);

  const postMessage = async (message) => {
    setLoader(true);
    try {
      // Adjust this endpoint to include language selection
      const response = await axios.post("http://127.0.0.1:8000/query", {
        message: message,
        chat_history: formatChats(chatHistory),
        output_language: selectedLanguage, // Include selected language
      });
      
      if (response.status === 200) {
        setLoader(false);
        setChatHistory((prevChatHistory) => ([
          ...prevChatHistory,
          response.data
        ]));
      } else {
        setLoader(false);
      }
    } catch (err) {
      setLoader(false);
      console.log(err);
    }
  };

  
  const createChat = async (message) => {

    setLoader(true);
    try {
      const response = await axios.post("http://127.0.0.1:8000/chats", {
        message: message,
      });
      if (response.status === 200) {
        
        
        const newchatId = response.data.id; // Assuming the UUID is returned in the response
        
        // Redirect to the new chat page with the extracted UUID
        navigate(`/c/${newchatId}`);
        message.chat_id = newchatId
        setChatHistory([message]);
        setLoader(true);
        postMessage(message);

        setLoader(false);
      } else {
        setLoader(false);
      }
    } catch (err) {
      setLoader(false);
      console.log(err);
    }
  };  

  const handleStop = async (blobUrl) => {
    setLoader(true);

    try {
      fetch(blobUrl);

      // Fetch audio blob
      const res = await fetch(blobUrl);
      const blob = await res.blob();

      // Construct FormData
      const formData = new FormData();
      formData.append("file", blob, "myFile.wav");

      // send audio to the backend, receive message
      const response = await axios.post(
        "http://127.0.0.1:8000/post-audio",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } } // Change content type to multipart/form-data
      );
      // append message to chat
      if (response.status === 200) {
        const cur_message = {
          text: response.data.response,
          sender: "user",
          id: uuid(),
          chat_id: chatId,
          created_at: Date.now(),
          updated_at: Date.now(),
        };
        if (chatId !== undefined) {
          setChatHistory((prevChatHistory) => [
            ...prevChatHistory,
            cur_message,
          ]);

          if (response.data.status == "400") {
            setLoader(false);
          } else if (response.data.response.status !== "400") {
            postMessage(cur_message);
          }
        } else {
          createChat(cur_message);
        }
      } else {
        console.log("in error; response : ", response.data.response);
        setLoader(false);
      }
    } catch (err) {
      setLoader(false);
      console.log(err);
    }
  };

  const onPressEnter = (e) => {
    setMessage(e.value);

    if (e.key === "Enter") {
      const cur_message = {
        text: e.target.value,
        sender: "user",
        id: uuid(),
        chat_id: chatId,
        created_at: Date.now(),
        updated_at: Date.now(),
      };
      if (chatId !== undefined) {
        setChatHistory((prevChatHistory) => [...prevChatHistory, cur_message]);
        postMessage(cur_message);
        setMessage("");
      } else if ((e.key === "Enter") & (chatId == undefined)) {
        createChat(cur_message);
        setMessage("");
      }
    }
  };

  const handleReportClick = (message_id) => {
    setSelectedmessage_id(message_id);
    setShowReportPopup(true);
  };

  
  const handleReportSubmit = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/report", {
        message_id: selectedmessage_id,
        description: reportDescription,
      });
      // Handle response as needed
      console.log("Report submitted successfully");
    } catch (error) {
      console.error("Error submitting report:", error);
    }
    setShowReportPopup(false);
    setSelectedmessage_id(null);
    setReportDescription("");
  };

  const handleReportCancel = () => {
    setShowReportPopup(false);
    setSelectedmessage_id(null);
    setReportDescription("");
  };

  return (
    <div>
      <div class="wrapper" >
        <ul class="chat-ul" ref={chatContainerRef}>
          {chatHistory.length === 0 && !loader && (<div class="chat-placeholder"> Type a message and press enter to send message or hold a mic to record...  </div>)}
          
          {chatHistory.map((message, index) => (
            <li key={index}>
              <div
              class={
                message.sender === "user" ? "chat-li-left" : "chat-li-right"
              }
              >
                {message.text}
              </div>
              { message.sender !== "user" ? 
                <div class="report-button" onClick={() => handleReportClick(message.id)}>
                  <DislikeOutlined style={{ color: "red" }} />
                </div>
              : ""}
            </li>
          ))}
        </ul>
      </div>
      <Row className="input-row">
        <Col className="align-center" span={2}>
          <RecordIcon handleStop={handleStop} loader={loader} />
        </Col>
        <Col span={20}>
          {loader == true ? (
            <div style={{ position: "relative" }}>
              <div
                style={{ position: "absolute", right: "15px", top: "10px" }}
                class="loader"
              ></div>
            </div>
          ) : null}

          <input
            disabled={loader}
            value={message}
            onKeyDown={onPressEnter}
            className="mesage-text"
            type="text"
          />
        </Col>
        <Col span={2} className="language-dropdown">
          <select
            disabled={loader}
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
          >
            <option value="english">English</option>
            <option value="arabic">Arabic</option>
            {/* Add more language options as needed */}
          </select>
        </Col>
      </Row>
      {showReportPopup && (
        <div className="report-popup">
          <h3 class="report-button-heading"> Submit Report</h3>
          <textarea
            value={reportDescription}
            onChange={(e) => setReportDescription(e.target.value)}
            placeholder="Add Optional Description about the issue."
          />
          <div>
            <button onClick={handleReportSubmit}>Submit</button>
            <button onClick={handleReportCancel}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Chats;