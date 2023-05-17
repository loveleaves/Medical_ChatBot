const recorderManager = wx.getRecorderManager()     //这是录音功能的实例，必须的
const innerAudioContext = wx.createInnerAudioContext();     //这是播放录音功能需要的实例

const app = getApp();
var inputVal = '';
var msgList = [];
var windowWidth = wx.getSystemInfoSync().windowWidth;
var windowHeight = wx.getSystemInfoSync().windowHeight;
var keyHeight = 0;

let socketOpen = false;
let socketMsgQueue = [];
let lineCount = Math.floor(windowWidth / 16) - 6;
let curAnsCount = 0;
/**
 * 初始化数据
 */
function initData(that) {
  inputVal = '';
  msgList = [{
    speaker: 'server',
    contentType: 'text',
    content: 'static/audio/greet.mp3'
  }, ]
  that.setData({
    msgList,
    inputVal
  })
  innerAudioContext.src = 'static/audio/greet.mp3';
  this.playVoice();
}

function sendSocketMessage(that, msg) {
  return new Promise((resolve, reject) => {
    // 以下用于文本问答，暂时弃用
    wx.request({
      url: '#', //  your server address
      method: "post",
      data: {
        "text_list": msg
      },
      success: ({
        data
      }) => {
        let res = data.data[0]['string'];
        that.setData({
          result: res
        })
        // console.log(that.data.result);
        resolve(res);
      },
      fail: (error) => {
        reject(error);
      }
    })
  });
}

Page({
  /**
   * 页面的初始数据
   */
  data: {
    scrollHeight: '100vh',
    inputBottom: 0,
    result: '', // 暂存返回结果
    tempFilePath: '', //存放录音文件的临时路径
    // ansFilePath: '', //存放回答文件的临时路径
    recordState: false, //记录按键状态
    playState: false, //记录播语音放状态
  },
  saveBaseAudioFile: function(base_data) {
    /*code是指图片base64格式数据*/
    //声明文件系统
    const fs = wx.getFileSystemManager();
    const self = this;
    //随机定义路径名称
    var times = new Date().getTime();
    var file_path = wx.env.USER_DATA_PATH + '/' + times + '.mp3';
    //将base64数据写入
    // var that = this;
    fs.writeFile({
      filePath: file_path,
      data: base_data,
      encoding: 'base64',
      success: (res) => {
        console.log(res)
        console.log(file_path)
        // 更新页面显示
        msgList.push({
          speaker: 'server',
          contentType: 'text',
          content: res.file_path
        });
        // console.log("录音结束时的语音文件",this.data.tempFilePath)
        self.setData({
          msgList,
          // ansFilePath: res.file_path
        });
        innerAudioContext.src = file_path;
        self.playVoice();
      }
    });
  },
  // 播放录音
  playVoice: function(e) {
    this.setData({
      playState: true
    })
    innerAudioContext.onPlay(() => {
      console.log('开始播放')
    })
    innerAudioContext.onError((res) => {
      console.log(res.errMsg)
      console.log(res.errCode)
      this.setData({
        playState: false
      })
    })
    innerAudioContext.play();

  },
  // 点击播放录音
  clickPlayVoice: function(e) {
    console.log(e.target.dataset.filepath);
    if(this.data.playState===true) {
      innerAudioContext.stop() // 停止
      this.setData({
        playState: false
      })
    } else {
      innerAudioContext.src = e.target.dataset.filepath;
      this.playVoice();
    }
  },
  // 录音
  beginRecord:function(e) {
    // 监听录音开始事件
    recorderManager.onStart(() => {
      console.log('recorder start')
      this.setData({
        recordState : true, 
        voice_ing_start_date: new Date().getTime(), //记录开始点击的时间
      })
    })
    // 监听已录制完指定帧大小的文件事件。如果设置了 frameSize，则会回调此事件。
    recorderManager.onFrameRecorded((res) => {
      const { frameBuffer } = res
      console.log('frameBuffer.byteLength', frameBuffer.byteLength)
    })
    //录音的参数
    const options = {
      duration: 20000,  //录音时间，默认是60s，提前松手会触发button的bindtouchend事件，执行停止函数并上传录音文件。超过60s不松手会如何并未测试过
      sampleRate: 16000, //44100
      numberOfChannels: 1,
      encodeBitRate: 24000, //192000
      format: 'wav',      //录音格式，这里是mp3
      // frameSize: 50    //指定帧大小，单位 KB。传入 frameSize 后，每录制指定帧大小的内容后，会回调录制的文件内容，不指定则不会回调。暂仅支持 mp3 格式。
    }
    //开始录音
    recorderManager.start(options); 

  },
  //停止录音并上传数据
  endRecord:function(e) {
    // const self = this;
    //停止录音
    recorderManager.stop();
    //监听录音停止事件，执行上传录音文件函数
    
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    initData(this);
    // this.setData({
    //   cusHeadIcon: "/images/春日野穹.png",
    // });
    // 录音停止事件
    recorderManager.onStop((res) => {
      console.log('recorder stop', res)

      //返回值res.tempFilePath是录音文件的临时路径 (本地路径)    
      this.setData({
        tempFilePath: res.tempFilePath,
        recordState: false
      })

      // 更新页面显示
      msgList.push({
        speaker: 'customer',
        contentType: 'text',
        content: res.tempFilePath
      });
      // console.log("录音结束时的语音文件",this.data.tempFilePath)
      this.setData({
        msgList
      });

      // innerAudioContext.src = res.tempFilePath
      //上传录音文件

      var x = new Date().getTime() - this.data.voice_ing_start_date
      if (x < 1000) {
        console.log('录音停止，说话时间小于1秒！')
        wx.showModal({
          title: '提示',
          content: '说话要大于1秒！',
          showCancel: false,
          success(res) {
            if (res.confirm) {
              console.log('用户点击确定')
            }
          }
        })
      } else if(x > 20000) {
        console.log('录音自动停止，说话时间大于20秒！')
        wx.showModal({
          title: '提示',
          content: '说话时间大于20秒！',
          showCancel: false,
          success(res) {
            if (res.confirm) {
              console.log('用户点击确定')
            }
          }
        })
      } else {
          var uploadTask = wx.uploadFile({
            //没有method，自动为POST请求
            filePath: res.tempFilePath,
            name: 'recordFile',                  //Flaks端接收数据的键
            url: '#', // 填写自己服务器的地址。
            header: {
              "Content-Type": "multipart/form-data" //必须是这个格式
            },
            formData:{
              username: "admin"
            },
            success:(e) => {
              console.log('succeed!');
              console.log(e.data);
              this.saveBaseAudioFile(e.data);
              // innerAudioContext.src = "data:audio/mp3;base64, " + e.data;
            //  this.playVoice();
            },
            fail: (e) => {
              console.log('failed!');
              console.log(e);   
            }
          });
          uploadTask.onProgressUpdate((e) => {
            console.log(e);
            console.log('期望上传的总字节数：' + e.totalBytesExpectedToSend);
            console.log('已经上传的字节数' + e.totalBytesSent);      
          })
      }
    })
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    socketOpen = true;
    console.log("打开socket");
    wx.showToast({
      icon: 'none',
      title: '会话建立成功',
      duration: 500
    })
  },
  onHide: function () {
      console.log("socket关闭成功");
      wx.showToast({
        icon: 'none',
        title: '会话关闭成功',
        duration: 500
      })

  },
  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 获取聚焦
   */
  focus: function (e) {
    let res = wx.getSystemInfoSync()
    let navBarHeight = res.statusBarHeight + 44 //顶部状态栏+顶部导航，大部分机型默认44px
    keyHeight = e.detail.height - navBarHeight;
    if (keyHeight < 0) {
      keyHeight = 0
    }
    this.setData({
      scrollHeight: (windowHeight - keyHeight) + 'px'
    });
    this.setData({
      toView: 'msg-' + (msgList.length - 1),
      inputBottom: (keyHeight) + 'px'
    })
  },

  //失去聚焦(软键盘消失)
  blur: function (e) {
    this.setData({
      scrollHeight: '100vh',
      inputBottom: 0
    })
    this.setData({
      toView: 'msg-' + (msgList.length - 1)
    })

  },

  /**
   * 发送点击监听
   */
  async sendClick(e) {
    try {
      await sendSocketMessage(this, e.detail.value);
      msgList.push({
        speaker: 'customer',
        contentType: 'text',
        content: e.detail.value
      });
      msgList.push({
        speaker: 'server',
        contentType: 'text',
        content: this.data.result
      })
      inputVal = '';
      this.setData({
        msgList,
        inputVal
      });
    } catch (error) {
      console.error(error);
    }
  },

  /**
   * 退回上一页
   */
  toBackClick: function () {
    wx.navigateBack({})
  }

})