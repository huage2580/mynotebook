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
 var that = this;
    const query = Bmob.Query("chapter");
    query.equalTo("bookid", "==", "386e6383ba");
    query.limit(500);
    // query.skip(500); 
    query.find().then(res => {
      // console.log(res)
      var group = []
      for(var index in res){
        var temp = res[index].c_name.split(' ')[0];
        if (!group.hasOwnProperty(temp)){
            group[temp] = res[index];
        }
      }
      for(var k in group){
        console.log(k)
      }
    });
```
    
