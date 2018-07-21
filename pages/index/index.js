//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    motto: 'Hello World',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },
  //事件处理函数
  bindSequence: function() {
    wx.navigateTo({
      url: '../question/question?type=sequence'
    })
  },
  bindRandom: function () {
    wx.navigateTo({
      url: '../question/question?type=random'
    })
  },
  bindFavorite: function () {
    let favorite_list = wx.getStorageSync('favorite_list')
    if (!favorite_list) {
      wx.showModal({
        title: 'Oops!',
        content: '你没有收藏的问题'
      })
      return
    }
    wx.navigateTo({
      url: '../question/question?type=favorite'
    })
  },
  about: function(){
    wx.navigateTo({
      url: '../about/about'
    })
  }

})
