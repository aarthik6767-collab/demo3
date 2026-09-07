const messages = document.getElementById("messages");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const welcome = document.getElementById("welcome");
const newChat = document.getElementById("newChat");
const clearChat = document.getElementById("clearChat");

function timeNow(){
  return new Date().toLocaleTimeString([], {hour:"2-digit", minute:"2-digit"});
}

function addMessage(text, who="bot", crisis=false){
  welcome.style.display = "none";
  const row = document.createElement("div");
  row.className = `msg ${who} ${crisis ? "crisis" : ""}`;
  row.innerHTML = `
    <div class="avatar">${who === "user" ? "●" : "✦"}</div>
    <div>
      <div class="bubble">${escapeHtml(text).replace(/\n/g,"<br>")}</div>
      <div class="meta">${who === "user" ? "You" : "MindMate"} · ${timeNow()}</div>
    </div>`;
  messages.appendChild(row);
  scrollBottom();
}

function escapeHtml(str){
  return str.replace(/[&<>"']/g, m => ({
    "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"
  }[m]));
}

function scrollBottom(){
  const box = document.getElementById("chatContent");
  setTimeout(()=> box.scrollTop = box.scrollHeight, 30);
}

function showTyping(){
  const row = document.createElement("div");
  row.className = "msg bot";
  row.id = "typing";
  row.innerHTML = `<div class="avatar">✦</div><div><div class="bubble"><div class="typing"><i></i><i></i><i></i></div></div></div>`;
  messages.appendChild(row);
  scrollBottom();
}

async function sendMessage(text){
  text = (text || input.value).trim();
  if(!text) return;
  input.value = "";
  input.style.height = "auto";
  addMessage(text, "user");
  showTyping();
  sendBtn.disabled = true;

  try{
    const res = await fetch("/chat", {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({message:text})
    });
    const data = await res.json();
    document.getElementById("typing")?.remove();
    addMessage(data.reply, "bot", data.crisis);
  }catch(err){
    document.getElementById("typing")?.remove();
    addMessage("I couldn't connect right now. Please try again.", "bot");
  }finally{
    sendBtn.disabled = false;
    input.focus();
  }
}

sendBtn.addEventListener("click", ()=>sendMessage());
input.addEventListener("keydown", e=>{
  if(e.key==="Enter" && !e.shiftKey){
    e.preventDefault();
    sendMessage();
  }
});
input.addEventListener("input", ()=>{
  input.style.height = "auto";
  input.style.height = Math.min(input.scrollHeight, 100) + "px";
});

document.querySelectorAll("[data-message]").forEach(btn=>{
  btn.addEventListener("click", ()=>sendMessage(btn.dataset.message));
});

function resetChat(){
  messages.innerHTML = "";
  welcome.style.display = "";
  input.value = "";
  input.focus();
}
newChat.addEventListener("click", resetChat);
clearChat.addEventListener("click", resetChat);

input.focus();
