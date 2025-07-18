let token="";

async function login(){
  const username=document.getElementById("username").value;
  const password=document.getElementById("password").value;

  const res=await fetch("http://127.0.0.1:8000/login", {
    method:"POST",
    headers:{"Content-Type": "application/json"},
    body:JSON.stringify({ username, password })
});

if (res.ok){
    const data = await res.json();
    token = data.access_token;
    alert("Login successful");

    document.getElementById("login-box").style.display = "none";
    document.getElementById("vault-box").style.display = "block";
  }
  else{
    alert("Login failed");
  }
}

async function storePassword(){
  const service=document.getElementById("service").value;
  const vaultUsername=document.getElementById("vault-username").value;
  const vaultPassword=document.getElementById("vault-password").value;

  const res=await fetch("http://127.0.0.1:8000/store", {
    method:"POST",
    headers:{
      "Content-Type":"application/json",
      "token":token
    },
    body:JSON.stringify({
      service:service,
      username:vaultUsername,
      password:vaultPassword
    })
  });

  if(res.ok) {
    alert("Password stored successfully!");
    loadVault();
  }
  else{
    alert("Failed to store password");
  }
}

async function loadVault(){
  const res = await fetch("http://127.0.0.1:8000/vault",{
    method: "GET",
    headers: {"token": token}
});

  if(res.ok){
    const data=await res.json();
    const vault=data.vault;

    const vaultDiv=document.getElementById("vault-output");
    vaultDiv.innerHTML="";

    vault.forEach(entry=>{
      vaultDiv.innerHTML += `
        <div>
          <strong>Service:</strong> ${entry.service}<br>
          <strong>Username:</strong> ${entry.username}<br>
          <strong>Password:</strong> ${entry.password}
          <hr />
        </div>
      `;
    });
  }
  else{
    alert("Failed to fetch vault");
  }
}
async function shredVault(){
  const confirmDelete = confirm("Are you sure you want to permanently delete all stored passwords?");
  if(!confirmDelete) return;

  const res = await fetch("http://127.0.0.1:8000/shred",{
    method: "DELETE",
    headers: {"token": token}
  });

  if(res.ok){
    alert("All passwords shredded");
    document.getElementById("vault-output").innerHTML = "";
  }
  else{
    alert("Failed to shred vault");
  }
}
