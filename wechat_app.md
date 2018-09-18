app.js
```
Bmob :{},
  onLaunch: function () {
    var Bmob_1 = require('/dist/Bmob-1.6.3.min.js');
    Bmob_1.initialize("363946ecc5bd0479fb7e923469f13796", "dc96a65d01aca996d57e373dd922127c");
    this.Bmob = Bmob_1;
```
page.js
```
const Bmob = getApp().Bmob;
```
    
    
