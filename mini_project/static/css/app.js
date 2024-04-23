const inputs = document.querySelectorAll(".input");

function focusFunc() {
  let parent = this.parentNode;
  parent.classList.add("focus");
}

function blurFunc() {
  let parent = this.parentNode;
  if (this.value == "") {
    parent.classList.remove("focus");
  }
}

inputs.forEach((input) => {
  input.addEventListener("focus", focusFunc);
  input.addEventListener("blur", blurFunc);
});


function sendMail() {
  var fn = document.forms["myform"]["fuser"].value;
  var umail = document.forms["myform"]["fmail"].value;
  var uph = document.forms["myform"]["fphone"].value;
  var umssg = document.forms["myform"]["fmessage"].value;

  if (fn == "" || fn == null) {
    alert('Please,fill all the details!! ')
    return false;
  }
  else if (umail == "" || umail == null) {
    alert('Please,filled all the details!! ')
    return false;
  }
  else if (uph == "" || uph == null) {
    alert('Please,filled all the details!! ')
    return false;
  }
  else if (umssg == "" || umssg == null) {
    alert('Please,filled all the details!! ')
    return false;
  }
  else {
    var params = {
      from_name: document.getElementById("name").value,
      email_id: document.getElementById("email").value,
      contact: document.getElementById("phone").value,
      message: document.getElementById("message").value
    };
    emailjs.send('service_d3vc1ip', 'template_2wgsa0n', params).then(function (response) {
      if (response.status == 200) {
        alert('Successfully Sent!')
      }
    }
      , function (error) {
        if (error.status == 400) {
          alert('Failed!')
        }
      }
    )
  }
}



function sendfeed() {
  var fop = document.forms["myfeed"]["fecm"].value;
  var fop = document.forms["myfeed"]["febr"].value;
  var fen = document.forms["myfeed"]["fename"].value;
  var femail = document.forms["myfeed"]["femail"].value;
  var fecmm = document.forms["myfeed"]["fmsg"].value;

  if (fop == "" || fop == null) {
    alert('Please,select the option!!')
    return false;
  }
  else if (fen == "" || fen == null) {
    alert('Please,filled the name!! ')
    return false;
  }
  else if (femail == "" || femail == null) {
    alert('Please,filled the email!! ')
    return false;
  }
  else if (fecmm == "" || fecmm == null) {
    alert('Please,write the message! ')
    return false;
  }
  else {
    var params = {
      report: document.getElementById('fdcm').value,
      report: document.getElementById('fdbr').value,
      from_name: document.getElementById("fdname").value,
      email_id: document.getElementById("fdmail").value,
      message: document.getElementById("fdmsg").value,
    };
    emailjs.send('service_lq6r9l4', 'template_pcf2s18', params).then(function (response) {
      if (response.status == 200) {
        alert('Successfully Sent!')
      }
    }
      , function (error) {
        if (error.status == 400) {
          alert('Failed!')
        }
      }
    )
  }
}
