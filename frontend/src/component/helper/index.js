export const formatChats = (chatData) => {
    let formattedChat = '';
  
    let currentHumanMessage = null;
    Object.keys(chatData).forEach(key => {
      if (key.startsWith("human")) {
        if (currentHumanMessage) {
          formattedChat += `\nHuman: ${currentHumanMessage}\nAI: ${chatData[key]}`;
          currentHumanMessage = null;
        } else {
          currentHumanMessage = chatData[key];
        }
      } else {
        formattedChat += `\nAI: ${chatData[key]}`;
      }
    });
  
    return [formattedChat];
  }