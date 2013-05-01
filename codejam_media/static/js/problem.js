
function preview_problem () {
	var name = tagName.value;
	var body = document.getElementById('problem_body').value;
	document.getElementById('dsb-problem-title-div').innerHTML = '<span style="color:#666">Problem A.</span>&nbsp&nbsp' + name;
	document.getElementById('dsb-problem-content-div0').innerHTML = body;
}

function confirm_delete() {
	return confirm ("Are you really want to delete problem?");
}

var LGCJ = LGCJ || {}

LGCJ.main = function () {

  function getNameFromFile() {
    var path = document.getElementById('problem_pdf').value;
    var idx = path.lastIndexOf('/');
    if (idx === -1) {
      idx = path.lastIndexOf('\\');
    }
    idx = Math.max(idx+1, 0);
    var ext = path.lastIndexOf('.pdf');
    return path.substring(idx, ext);
  }
  
  
  
  var tagName = document.getElementById('problem_name');
  /*if (tagName) {

    tagName.onchange = function () {
      if (this.value.length === 0) {
        this.value = getNameFromFile();
      }
    }
  
    tagName.onkeypress = function (event) {
      if (event.keyCode == 13) {
        return false;
      }
    }
    
  }*/ // tagName
  
  var tagPdf = document.getElementById('problem_pdf');
  if (tagPdf) {
    
    var tagTitle = document.getElementById('problem_title');
    tagPdf.onchange = function () {
      var name = getNameFromFile();
      if (tagTitle) {
        tagTitle.innerHTML = name;
      }
      var nameTag = tagName;
      if (nameTag.value.length === 0) {
        nameTag.value = name;
      }
    }

  } // tagPdf
  
  var tagTitle = document.getElementById('problem_title');
  /*if (tagTitle) {
    
    tagTitle.onclick = function () {
      tagName.type = 'text';
      this.style.display = 'none';
    }
    
  }*/ // tagTitle

  var tagPoints = document.getElementById('problem_points');
  if (tagPoints) {
    var points = tagPoints.value;
  
    tagPoints.onchange = function () {
      var tmp = Number(this.value);
      if (isNaN(tmp)) {
        alert('[Error] It\'s not a integer number.');
        this.value = points;
        return;
      }
      tmp = Math.floor(tmp);
      if (tmp < 1) {
        alert('[Error] Point(s) maust greater than 1.');
        this.value = points;
        return;
      }
      this.value = tmp;
    }
    
    tagPoints.onkeypress = function (event) {
      if (event.keyCode == 13) {
        return false;
      }
    }

  } // tagPoints
  
  document.getElementById('problem_create').onsubmit = function () {
    if (!modify) {
      var value = document.getElementById('problem_pdf').value;
      if (value.length < 4) {
        alert('[Error] Please select a PDF file to upload.');
        return false;
      }
    }
  }



  var tagPdfName = document.getElementById('pdf_name');
  if (tagPdfName) {
    
    var tagPdfBlock = document.getElementById('problem_pdf_block');
    tagPdfName.onclick = function () {
      document.getElementById('problem_pdf_cancel').onclick = function () {
        tagPdfBlock.style.display = 'none';
        tagPdfName.style.display = 'block';
        tagPdf.value = '';
        return false;
      }
      tagPdfBlock.style.display = 'block';
      tagPdfName.style.display = 'none';
    }
    
  } // tagPdfName
  
}
