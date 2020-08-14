function add_new(){
  $("#input-image-new").bind("change", function(){
    let fileData=$(this).prop("files")[0];
    if(typeof (FileReader) != "undefined"){
        let imagePreview=$("#image-avatar");
        imagePreview.empty();// làm rỗng ;
        let fileReader=new FileReader();
        fileReader.onload=function(element){
          let avtPreview = `<img src="${element.target.result}" id = "src-to-img" style="width: 150px; height: 150px;" class="" alt="avatar">`
          $("#image-avatar").append(avtPreview)
        }
        imagePreview.show();
        fileReader.readAsDataURL(fileData);
        filename = fileData.name
    } else{
        return false
    }
  })
  $("#input-btn-save").bind("click", function(){
    let username = $("#input-username").val()
    let year = $("#input-year-born").val()
    let phone = $("#input-phone").val()
    let img_src = $("#src-to-img").attr("src")

    let data = JSON.stringify({
      username : username,
      year : year, 
      phone : phone,
      img : img_src
    })
    $(".test_data").attr("value", data)
  })


  $("#input-btn-cancel").bind("click", function(){
    $("#input-username").val(null)
    $("#input-year-born").val(null)
    $("#input-phone").val(null)
    $("#input-image-new").val(null)
    $("#image-avatar").empty()
  })
}

$(document).ready(function(){
  add_new()
})