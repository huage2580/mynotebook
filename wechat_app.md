app.js
```
Bmob :{},
  onLaunch: function () {
    var Bmob_1 = require('/dist/Bmob-1.6.3.min.js');
    Bmob_1.initialize("****", "****");
    this.Bmob = Bmob_1;
```
page.js
```
const Bmob = getApp().Bmob;
```
获取章节
```
Page({
  //章节
  allChapter : new Array(),
  allCount : 0,
  
  //*****************************
  onLoad: function (options) {
    var that = this;
    const query = Bmob.Query("chapter");
    query.equalTo("bookid", "==", "386e6383ba");
    query.count().then(res => {
      this.allCount = res;
      loadChapter(this,0);
    });
    
  }
  //------------------------------------------------
  function loadChapter(that,i) {
    const query = Bmob.Query("chapter");
    query.equalTo("bookid", "==", "386e6383ba");
    query.limit(500);
    query.skip(500 * i);
    query.find().then(res => {
      // console.log(res)
      that.allChapter = that.allChapter.concat(res);
      if (500 * (i + 1) < that.allCount) {
        loadChapter(that,i + 1);
      } else {
        genGroup(that);
      }
    });
  }

function genGroup(that) {
  var group = []
  // console.log(that.allChapter);
  for (var index in that.allChapter) {
    var temp = that.allChapter[index].c_name.split(' ')[0];
    if (!group.hasOwnProperty(temp)) {
      group[temp] = that.allChapter[index];
    }
  }
  for (var k in group) {
    console.log(k)
  }
}
```
    
