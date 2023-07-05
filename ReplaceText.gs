function replaceText() {
  let tr = '{ "我们的基金公司" : "Our Fundhouses", "我们的业务合作伙伴" : "Our Business Partners"}';
  var trn = JSON.parse(tr);
  var slides = SlidesApp.getActivePresentation().getSlides();
  // var activeSlide = SlidesApp.getActivePresentation().getActiveSlide();
  var fundHouse = slides[0];
  // ID = editor-g22ec9073485_0_579
  var content = fundHouse.getPageElementById('g22ec9073485_0_579').asShape();
  var text = content.getText();
  //for(var i in trn){
    //console.log(trn[i]);
  //}
  try{
    for(var i in trn){
      console.log("%s", i);
      text.replaceAllText(i, trn[i]);
      //if(text.search(i)!=-1){
        //text.setText(trn[i]);
        //break;
      //}
    }
    
    // a = a.toString().replace();
    console.log("Yurr");
  } catch(err) {
    console.log('FAILURE!');
  }
}
