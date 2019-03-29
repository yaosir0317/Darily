var Host = window.location.protocol + '//' + window.location.host + '/';
var timeoutId, checkTryTimes = 0, breatheTimes = 4, date = new Date, curHour = date.getHours();
var Urls = {
  // 拆分该接口为三个独立接口
  recommendKeywords: Host + 'data/loc/recommend_keywords',
  // 1. TODO 定位历史接口
  historyKeywords: Host + 'jd_rank/history_keywords',
  // 2. TODO 到店词

  // 3. TODO 我的收藏词

  // 已经完成OK
  checkLocKeywords: Host + 'jd_rank/check_keyword_log',
  // 全店关键词搜索列表
  searchLocKeywordSkuList: Host + 'jd_rank/search_keyword_sku_list',
  // 已经完成OK
  addKeywordGroup: Host + 'jd_rank/add_keyword_group',
  // 已经完成OK
  cancelLocKeyword: Host + 'jd_rank/cancel_keyword',
  // 已经完成OK
  countLocKeywordPromoSku: Host + 'jd_rank/count_keyword_promo',
  // 删除定位历史
  delKeywordHistoryGroup: Host + 'jd_rank/del_history_keywords'
}, $G = {}, keywordBox = [], taskMap = [], locSkuList = [], locRunning = false;

// 通用操作
var keywordOptions = {
  // 重置搜索框
  resetBox: function () {
    keywordBox = [], taskMap = [];
    $('.J_queryKeywordList').find('.J_keyword').remove();
    $('#J_locKeywordTaskList').find('.J_locKeywordLabel').remove();
  },
  // 添加关键词到搜索框
  addKeywordsToBox: function (keyword) {
    var keyword = $.trim(keyword), keyword = keyword.toString();
    if (_.isEmpty(keyword) || ($.inArray(keyword, keywordBox) !== -1)) {
      return false;
    }
    var maxKeyword = 12;
    if (keywordBox.length == maxKeyword) {
      layer.alert("一次最多只能输入" + maxKeyword + "个关键词");
      return false;
    }
    keywordBox.push(keyword);
    this.buidHtml();
  },
  // 搜索框清除关键词
  removeKeywordsFromBox: function (keyword) {
    var keyword = $.trim(keyword), keyword = keyword.toString();
    var idx = $.inArray(keyword, keywordBox);
    if (_.isEmpty(keyword) || (idx === -1)) {
      return false;
    }
    keywordBox.splice(idx, 1);
    this.buidHtml();
  },
  // 搜索框，输入关键词样式构建
  buidHtml: function () {
    var qhtml = '';
    if (keywordBox.length == 0) {
      $('.J_queryKeywordList').html('');
    }
    keywordBox.forEach(function (tmpKeyword) {
      if (_.isEmpty(tmpKeyword)) {
        return;
      }
      var keywordHtml = _.template('<span class="tag label label-info J_keyword" data-keyword="<%= locKeyword %>"><%= locKeyword %><span data-role="remove" data-keyword="<%= locKeyword %>"></span></span>')({
        locKeyword: tmpKeyword
      });
      qhtml += keywordHtml
    });
    $('.J_queryKeywordList').empty().html(qhtml);
  },
  // 关键词Label构建
  buildLocKeywordLabel: function (locId, keyword, process, webMatch, wxMatch, wapMatch, qqMatch, status) {
    var tpl = '<div class="col-xs-3 p-x J_locKeywordLabel m-b" id="J_locKeywordTask_<%= locId %>" data-loc-id="<%= locId %>">' +
      '  <div class="databox databox-shadowed animated zoomIn m-b-0">' +
      '    <div class="databox-left <%= (status == "success") ? "bg-green" : (status == "process" ? "bg-azure" : "bg-gray") %>">' +
      '      <div class="databox-piechart <%= (status == "process") ? "activity" : "" %>"></div>' +
      '      <div class="databox-process J_process"><%= process %>%</div>' +
      '    </div>' +
      '    <div class="databox-right">' +
      '      <span class="databox-number"><%= keyword %></span>' +
      '      <div class="databox-text darkgray truncate">PC:<span class="J_web fc-red"><%= webMatch %></span>个&nbsp;安卓:<span class="J_wap fc-red"><%= wapMatch %></span>个&nbsp;微信:<span class="J_wx fc-red"><%= wxMatch %></span>个&nbsp;QQ:<span class="J_qq fc-red"><%= qqMatch %></span>个<span class="J_promo loc-promo-tip m-l-sm" style="display:noen;"></span></div>' +
      '      <div class="databox-state J_state" style="display:none;"><i class="fa fa-check-circle fa-lg"></i></div>' +
      '      <a href="javascript:void(0);"  style="<%= (status == "process") ? "display:block;" : "display:none;"%>" class="databox-state J_cancelLocSearch fc-red" data-loc-id="<%= locId %>"><i class="fa fa-undo"></i></a>' +
      '    </div>' +
      '  </div>' +
      '</div>';
    var compiled = _.template(tpl)({
      'locId': locId,
      'keyword': keyword,
      'process': process > 0 ? process : 0,
      'webMatch': webMatch >= 0 ? webMatch : '--',
      'wxMatch': wxMatch >= 0 ? wxMatch : '--',
      'wapMatch': wapMatch >= 0 ? wapMatch : '--',
      'qqMatch': qqMatch >= 0 ? qqMatch : '--',
      'status': status
    });
    $('#J_locKeywordTaskList').append(compiled);
  },
  // 历史数据，搜索列表构建
  buildHistoryLable: function (keywordCnt, psortName, gmtLoc) {
    var paramHtml = _.template(
      '共定位<span class="fc-red lead ft_16"> <%= keywordCnt %> </span>' +
      '个关键词，排序：<span class="fc-red lead ft_16"> <%= psortName %> </span>' +
      '，定位时间：<span class="fc-red lead ft_16"> <%= gmtLoc %> </span></span>'
    )({
      'keywordCnt': keywordCnt,
      'psortName': psortName,
      'gmtLoc': gmtLoc
    });
    $('#J_locHistorySetting').empty().html(paramHtml).show();
  }
};

var initOptions = {
  init: function () {
    $G = initOptions;
    $G.searchbarInit();
    $G.showResultInit();
    $G.showHistory();
  },
  // 初始化搜索框
  searchbarInit: function () {
    // 搜索框，框内点击事件，触发下拉框，并阻止冒泡事件
    $('.dropdown > .dropdown-menu').on('click', function (e) {
      e.stopPropagation();
    });
    // 搜索框，框内点击事件，获取焦点
    $('.J_searchbarMain').on('click', function () {
      $('#J_enterKeyword').focus();
    });
    // 搜索框，获取焦点操作
    $('#J_enterKeyword').on('focusin', function () {
      $(this).closest('.bts-tagsinput').addClass('focus');
    });
    // 搜索框，失去焦点操作
    $('#J_enterKeyword').on('focusout', function () {
      $(this).closest('.bts-tagsinput').removeClass('focus');
    });
    // 关键词下拉框默认显示定位历史
    $('.J_searchbarMain').on('shown.bs.dropdown', function () {
      var target = $('.J_recommendKeywords > li.active > a').data('tab');
      // 历史数据值只显示10条
      $G.historyKeywords(target, 1)
    });
    // 下拉框TAB切换
    $('.J_recommendKeywords > li a').on('click', function (e) {
      e.preventDefault();
      $(this).tab('show');
    });
    // // TAB切换调用数据
    // $('.J_recommendKeywords > li a').on('shown.tab.bs', function () {
    //   var $this = $(this), target = $this.data('tab');
    //   $G.recommendKeywords(target, 1);
    // });
    // 搜索参数
    $('.J_setSearchParam').on('click', function () {
      var setting = $G.getValMap($('#J_locSetting input'));
      var paramHtml = _.template('<span class="fc-red"><%= sort %></span>，PC<span class="fc-red"><%= pc_max_page %></span>页，移动<span class="fc-red"><%= m_max_page %></span>页')({
        sort: $('#J_locSetting [name="sort"]:checked').data('name'),
        pc_max_page: setting['pc_max_page'],
        m_max_page: setting['m_max_page']
      });
      $('.J_searchParam').html(paramHtml);
      $('#J_locSetting').parent('.dropdown').removeClass('open');
    });
    // 下拉框，到店词推荐，添加按钮
    $('.J_recommendKeywordPanel').on('click', '.J_recommendKeywordLoc', function (e) {
      e.preventDefault();
      keywordOptions.addKeywordsToBox($(this).data('keyword'));
    });
    // 下拉框，定位历史，查看按钮
    $('.J_recommendKeywordPanel').on('click', '.J_getLocKeywordHistory', function (e) {
      e.preventDefault();
      var taskList = $(this).data('taskList'), locInfo = $(this).data('locInfo');
      if (taskList.length > 0) {
        historyTaskList = taskList;
        $G.showHistory();
        keywordOptions.buildHistoryLable(locInfo['keywordCnt'], locInfo['psortName'], locInfo['gmtLoc']);
        $('.J_searchbarMain').removeClass('open');
      }
    });
    // 下拉框，定位历史，定位按钮
    $('.J_recommendKeywordPanel').on('click', '.J_addKeywordToBox', function (e) {
      e.preventDefault();
      var taskList = $(this).data('taskList');
      if (taskList.length == 0) {
        return false;
      }
      keywordBox = [], taskMap = [];
      $('.J_queryKeywordList').find('.J_keyword').remove();

      $.each(taskList, function (i, task) {
        keywordOptions.addKeywordsToBox(task['keyword_name']);
      });
    });
    // 下拉框，定位历史，添加按钮
    $('.J_recommendKeywordPanel').on('click', '.J_appendKeywordToBox', function (e) {
      e.preventDefault();
      var taskList = $(this).data('taskList');
      if (taskList.length == 0) {
        return false;
      }
      $.each(taskList, function (i, task) {
        keywordOptions.addKeywordsToBox(task['keyword_name']);
      });
    });
    // 下拉框，定位历史，删除按钮
    $('.J_recommendKeywordPanel').on('click', '.J_delLocKeywords', function () {
      var groupId = $(this).data('groupId');
      $G.deleteLocKeywordGroup(groupId, function (ret) {
        if (ret.message_code == 20000) {
          var $target = $('#J_locKeywordHistory');
          $target.searchLoad({'min-height': '200px'});
          var target = $('.J_recommendKeywords > li.active > a').data('tab');
          $G.historyKeywords(target, 1);
        } else {
          var reason = isEmpty(ret['message']) ? '删除定位历史失败' : ret['message'];
          layer.alert(reason);
        }
      });
    });
    // 输入框清除输入关键词操作
    $('.J_queryKeywordList').on('click', '[data-role="remove"]', function () {
      keywordOptions.removeKeywordsFromBox($(this).data('keyword'));
    });
    // 搜索框，回车键，添加关键词操作
    $('#J_enterKeyword').on('keydown', function (e) {
      var keyword = $(this).val();
      if (e.keyCode == 13) {
        if (_.isEmpty(keyword)) {
          layer.alert("请先输入关键词，然后再回车完成，可添加多个关键词");
          return false;
        }
        keywordOptions.addKeywordsToBox(keyword);
        $(this).val('');
      }
      if (e.keyCode == 8 && _.isEmpty(keyword)) {
        var $kList = $(this).prev('.J_queryKeywordList');
        var $k = $kList.find('>.J_keyword:last'), keyword = $k.data('keyword');
        keywordOptions.removeKeywordsFromBox(keyword), $k.remove();
      }
    });
    // 搜索框，一键查排名操作
    $('#J_startLocKeyword').on('click', function () {
      var enterKeyword = $('#J_enterKeyword').val(), enterKeywords = [];
      !_.isEmpty(enterKeyword) && (enterKeywords = enterKeyword.split(/,|，/ig));
      enterKeywords.length && enterKeywords.forEach(function (tmpKeyword) {
        keywordOptions.addKeywordsToBox(tmpKeyword);
      });
      $('#J_enterKeyword').val('');
      $G.startLocKoywordBox();
    });
    // 添加搜索框输入的关键词到关键词Label
    if (keywordBox.length == 0 && $('.J_queryKeywordList .J_keyword').length > 0) {
      $('.J_queryKeywordList .J_keyword').each(function (i) {
        keywordOptions.addKeywordsToBox($(this).data('keyword'));
      });
    }
    // 关键词Label，取消该关键词任务
    $('#J_locKeywordTaskList').on('click', '.J_cancelLocSearch', $G.cancelLocKeyword);
  },
  // 初始化搜索结果
  showResultInit: function () {
    // 筛选操作
    $('.J_locFilterKeywordBtn').on('click', function () {
      $G.getLocResultData(1, 8);
    });
    // 关键词label，指定查询对应的排名信息
    $('#J_locKeywordTaskList').on('click', '.J_locKeywordLabel', function () {
      var $t = $(this), $box = $t.find('.databox'), locId = $t.data('locId');
      if (locRunning) {
        return;
      }
      if ($box.hasClass('active')) {
        $box.removeClass("active"),
          $box.find('.J_state').hide();
      } else {
        $.each(taskMap, function (i, v) {
          if ((v['locId'] == locId) && (v['status'] == 'success')) {
            $box.addClass('active');
            return false;
          }
        });
        $box.find('.J_state').show();
      }
      $G.getLocResultData(1, 8);
    });
  },
  // 初始化历史
  showHistory: function () {
    // 处理历史任务数据，后端直接渲染到页面
    if (historyTaskList.length > 0) {
      keywordOptions.resetBox();
      for (var i in historyTaskList) {
        var task = historyTaskList[i];
        // 如果任务成功 estimate=100，其他均为随机数
        var estimate = 100;
        if (task['task_status'] != 'success') {
          estimate = parseInt((Math.random() * 100).toString());
        }
        taskMap.push({
          'locId': task['keyword_id'],
          'keyword': task['keyword_name'],
          'process': estimate,
          'tryTimes': 0,
          'status': task['task_status']
        });
        // 构建关键词Label
        keywordOptions.buildLocKeywordLabel(
          task['keyword_id'], task['keyword_name'], estimate, task['hit_sku_num_web'],
          task['hit_sku_num_wx'], task['hit_sku_num_wap'], task['hit_sku_num_qq'], task['task_status']
        );
        // 历史推广数
        var $box = $('#J_locKeywordTask_' + task['keyword_id']);
        if ($box.length > 0) {
          task['ad_web'] > 0 ?
            $box.find('.J_promo').html(task['ad_web'] + ' 推广').show() :
            $box.find('.J_promo').hide();
        }
      }
      // 搜索列表数据调用
      $G.getLocResultData(1, 8);
    }
  },
  // 初始化查询关键词Label
  startLocKoywordBox: function () {
    if (keywordBox.length == 0) {
      layer.alert("请先输入关键词");
      return false;
    }
    if (locRunning == true) {
      layer.alert("定位正在运行，请完成之后操作");
      return false;
    }

    var iid = layer.load("正在初始化关键词");
    var locParams = $G.getValMap($('#J_locSetting input'));
    $.ajax({
      url: Urls.addKeywordGroup,
      data: {
        "keywords": keywordBox.toString(),
        'sort': locParams['sort'],
        'pc_max_page': locParams['pc_max_page'],
        'm_max_page': locParams['m_max_page']
      },
      method: 'post',
      dataType: 'json'
    }).always(function () {
      layer.close(iid);
    }).then(function (ret) {
      if (ret['result'] == 'fail') {
        layer.alert(ret['reason']);
        return false;
      }
      locRunning = true, breatheTimes = 0;
      $('#J_locKeywordTaskList').html('');
      $('#J_curLocPsortName').val(ret['psortName']);
      $('#J_curGtmLoc').val(ret['gmtLoc']);
      $('#J_curKeywordCnt').val(ret['keywordCnt']);
      $('#J_startLocKeyword').addClass('disabled').prop('disablde', true).html('<i class="fa fa-spinner fa-pulse fa-fw mr_5"></i>定位中 ...');

      var locInfo = ret['locInfo'];
      taskMap = [];
      for (var i in locInfo) {
        var loc = locInfo[i];
        keywordOptions.buildLocKeywordLabel(loc['local_id'], loc['keyword'], 0, 0, 0, 0, 0, loc['status']);
        taskMap.push({
          'locId': loc['local_id'],
          'keyword': loc['keyword'],
          'process': 0,
          'tryTimes': 0,
          'status': loc['status']
        });
      }
      $G.checkLocTaskFinish(function () {
        $G.getLocResultData(1, 8, function () {
          var keywordCnt = $('#J_curKeywordCnt').val(), psortName = $('#J_curLocPsortName').val(),
            gmtLoc = $('#J_curGtmLoc').val();
          keywordOptions.buildHistoryLable(keywordCnt, psortName, gmtLoc);
        });
        $G.tooltipBox();
        $G.tipPromoLocKeyword();
        $G.revertAction();
      });
    });
  },
  // 关键词Label 筛选提示框
  tooltipBox: function () {
    var $box = $('#J_locKeywordTaskList > .J_locKeywordLabel');
    $box.find('.databox').addClass('pointer'), $box.tooltip({
      title: "单击关键词标签，可单独查看该关键词的定位结果。"
    });
  },
  // 推广信息展示
  tipPromoLocKeyword: function () {
    var locIds = $G.getRunningLocIds();
    $.ajax({
      url: Urls.countLocKeywordPromoSku,
      data: {"local_ids": locIds.toString()},
      method: 'post',
      dataType: 'json'
    }).done(function (cRet) {
      if (cRet['result'] == 'fail') {
        return;
      }
      var promoCut = cRet['promoSkuCount'];
      $.each(promoCut, function (locId, cnt) {
        var $box = $('#J_locKeywordTask_' + locId);
        if ($box.length > 0) {
          cnt > 0 ? $box.find('.J_promo').html(cnt + ' 推广').show() : $box.find('.J_promo').hide();
        }
        ;
      });
    });
  },
  // 回调巡检任务进度
  checkLocTaskFinish: function (callback) {
    var locIds = $G.getRunningLocIds();
    if (locRunning == false) {
      return false;
    }

    if ((taskMap.length > 0) && (locIds.length == 0)) {
      $G.revertAction();
    }

    if ((locRunning == true) && (locIds.length == 0)) {
      timeoutId = setTimeout((function (callback) {
        return function () {
          $G.checkLocTaskFinish(callback);
        };
      })(callback), 10000);
      return false;
    }

    $.ajax({
      url: Urls.checkLocKeywords,
      data: {"local_ids": locIds.toString()},
      method: 'post',
      dataType: 'json'
    }).done(function (locRets) {
      breatheTimes++;
      var needWait = false;
      // 时间段处理
      if ((curHour >= 9) && (curHour <= 10)) {
        needWait = (breatheTimes < 4) ? true : false;
      }
      // 所有任务，最大超时时间
      var allTaskIsEnd = true, maxTimeout = (locIds.length * 80);
      // 判断每个关键词的状态
      $.each(locRets, function (locId, ret) {
        // 任务完成状态，取消，失败，删除
        if ($.inArray(ret['status'], ['cancel', 'fail', 'delete']) != -1) {
          if (ret['status'] == 'fail') {
            var $dom = $('#J_locKeywordTaskList').find('#J_locKeywordTask_' + locId);
            $dom.find('.databox-left.bg-azure').removeClass('bg-azure').addClass('bg-gray');
            $dom.find('.activity').removeClass('activity');
          }
          return;
        }

        var curLocId = locId;
        // TODO 变更数据对应字段
        var processWeb = (ret['process_web'] > 100) ? 100 : ret['process_web'];
        var processWx = (ret['process_wx'] > 100) ? 100 : ret['process_wx'];
        var processWap = (ret['process_wap'] > 100) ? 100 : ret['process_wap'];
        var processQq = (ret['process_qq'] > 100) ? 100 : ret['process_qq'];
        var estimate = parseInt((processWeb + processWx + processWap + processQq) / 4);

        if (estimate == 0) {
          checkTryTimes++
          // 超时处理
          if (checkTryTimes > maxTimeout) {
            // 回复默认状态，停止巡检
            $G.revertAction();
            layer.alert('定位超时，请重试或联系客服。');
            return false;
          }
        }

        var $dom = $('#J_locKeywordTaskList').find('#J_locKeywordTask_' + curLocId);
        if ($dom.length > 0) {
          if (needWait && estimate >= 100) {
            estimate = 99;
          }
          $dom.find('.J_process').html(estimate + '%');
          // TODO 动态更新命中数据
          $dom.find('.J_web').html(ret['hit_sku_num_web']);
          $dom.find('.J_wap').html(ret['hit_sku_num_wap']);
          $dom.find('.J_wx').html(ret['hit_sku_num_wx']);
          $dom.find('.J_qq').html(ret['hit_sku_num_qq']);
          if (estimate >= 100) {
            $G.endLocKeywordLable(locId);
          }
        }
        if ((ret['status_web'] != 'success') || (ret['status_wx'] != 'success') || (ret['status_wap'] != 'success')
          || (ret['status_qq'] != 'success')) {
          allTaskIsEnd = false;
        }
      })

      if ((allTaskIsEnd == true) && !needWait) {
        // 任务停止
        if ($.type(callback) == 'function') {
          // 启动回调函数
          callback(locRets);
        }
        return false;
      }

      timeoutId = setTimeout((function (callback) {
        return function () {
          $G.checkLocTaskFinish(callback);
        };
      })(callback), 3000);
    });
  },
  // 取消关键词查询操作
  cancelLocKeyword: function () {
    var $this = $(this), locId = $this.data('locId');
    if (locId <= 0) {
      layer.alert("参数错误");
      return false;
    }

    layer.confirm("您确定要取消定位该关键词吗？", function (index) {
      $.ajax({
        url: Urls.cancelLocKeyword,
        data: {"locId": locId},
        method: 'post',
        dataType: 'json'
      }).always(function () {
        layer.close(index);
      }).done(function (ret) {
        if (ret.result == 'success') {
          $.each(taskMap, function (i, v) {
            if (v.locId == locId) {
              taskMap[i]['status'] = 'cancel';
            }
          });
          var $dom = $('#J_locKeywordTaskList').find('#J_locKeywordTask_' + locId);
          $dom.find('.databox-left.bg-azure').removeClass('bg-azure').addClass('bg-gray');
          $dom.find('.activity').removeClass('activity');
        } else {
          layer.alert("定位任务取消失败");
        }
      });
    });
  },
  // 一键排名按钮状态恢复
  revertAction: function () {
    clearTimeout(timeoutId);
    checkTryTimes = 0;
    locRunning = false;
    $('#J_startLocKeyword').removeClass('disabled').prop('disabled', false).html('一键查排名');
  },
  // 关键词查询结束后Label样式更新
  endLocKeywordLable: function (locId) {
    var $dom = $('#J_locKeywordTaskList').find('#J_locKeywordTask_' + locId);
    $dom.find('.databox-piechart.activity').removeClass('activity');
    $dom.find('.databox-left.bg-azure').removeClass('bg-azure').addClass('bg-green');
    $dom.find('.J_cancelLocSearch').hide();
    $.each(taskMap, function (i, v) {
      if (v['locId'] == locId) {
        v['status'] = 'success';
        return false;
      }
    });
  },
  // 获取正在执行关键词ID
  getRunningLocIds: function () {
    var locIds = [];
    $.each(taskMap, function (i, v) {
      if (_.has(v, 'status') && $.inArray(v['status'], ['process', 'success']) != -1) {
        locIds.push(v['locId']);
      }
    })
    return locIds;
  },
  // 获取结果
  getLocResultData: function (page, pageSize, callback) {
    var page = page > 0 ? page : 1;
    var locIds = $G.getRunningLocIds(), selectedLocIds = [];
    $.each($('.J_locKeywordLabel'), function () {
      var locId = $(this).data('locId');
      if (locId > 0 && ($(this).find('.databox.active').length > 0)) {
        selectedLocIds.push(locId);
      }
    });
    if (selectedLocIds.length == 0) {
      selectedLocIds = locIds;
    }
    $G.searchLocKeywordSkuList(page, selectedLocIds, pageSize, callback);
  },
  // 本店商品查询结果
  searchLocKeywordSkuList: function (p, locIds, pageSize, callback) {
    var filterKeyword = $.trim($('#J_locFilterKeyword').val());
    var page = p > 0 ? p : 1;
    var load_id = layer.load();
    $.ajax({
      url: Urls.searchLocKeywordSkuList,
      data: {"page": page, "local_ids": locIds.toString(), "keyword": filterKeyword, "page_size": pageSize},
      method: 'get',
      dataType: 'json'
    }).always(function () {
      layer.close(load_id);
    }).done(function (ret) {
      if (!_.isEmpty(ret['results']) && ret['message_code'] == 20000) {
        locSkuList = ret['results'];
        // 分页处理
        layui.use('laypage', function () {
          var laypage = layui.laypage;
          laypage.render({
            elem: 'shopRankShowPage',
            count: ret['count'],
            limit: pageSize,
            limits: [8, 10, 15, 30, 50],
            curr: page,
            layout: ['count', 'prev', 'page', 'next', 'limit', 'refresh', 'skip'],
            jump: function (obj, first) {
              var locSkuHtml = '';
              for (var i in locSkuList) {
                var skuIdDict = locSkuList[i];
                locSkuHtml += '<div class="loc-result ' + "J_locSkuItem" + skuIdDict.sku_id + " J_locWareItem" + skuIdDict.ware_id + '">'
                locSkuHtml += '<div class="panel panel-default mb_10">'
                // <!-- 商品信息 -->
                locSkuHtml += '<div class="panel-body" style="padding:5px 10px;">'
                locSkuHtml += '<div class="row">'
                locSkuHtml += '<div class="col-xs-8">'
                locSkuHtml += '<div class="media">'
                locSkuHtml += '<div class="media-left">'
                locSkuHtml += '<a target="_blank" href="' + 'http://img10.360buyimg.com/n7/' + skuIdDict.logo + '" style="margin-bottom:0;">'
                locSkuHtml += '<img src="' + 'http://img10.360buyimg.com/n7/' + skuIdDict.logo + '" class="header-avatar" style="width:45px;height:45px;">'
                locSkuHtml += '</a></div>'
                locSkuHtml += '<div class="media-body pt_5 ft_12">'
                locSkuHtml += '<a href="' + 'https://item.jd.com/' + skuIdDict.sku_id + '.html"' + 'class="fc-slate-gray" target="_blank">' + skuIdDict.sku_name + ''
                locSkuHtml += '<span class="lead ft_12 red">"' + skuIdDict.ad_title + '"</span></a>'
                locSkuHtml += '<div class="mt_5 text-muted">'
                locSkuHtml += '<span class="mr_10">商品编码：<span class="lead ft_12">' + skuIdDict.ware_id + '</span></span>'
                locSkuHtml += '<span>SKU：<span class="lead ft_12">' + skuIdDict.sku_id + '</span></span>'
                locSkuHtml += '</div></div> </div> </div>'
                locSkuHtml += '<div class="col-xs-4">'
                locSkuHtml += '<div class="pull-right mt_10">'
                locSkuHtml += '<a href="javascript:void(0);" target="_blank" class="btn btn-default btn-sm">'
                locSkuHtml += '<i class="fa fa-map-marker mr_5"></i>单品查排名 </a> </div> </div> </div> </div>'
                // <!-- 排名数据 -->
                locSkuHtml += '<table class="table table-striped ft_12 table-condensed">'
                locSkuHtml += '<tbody>'
                var localHtml = ''
                // <!-- TODO 数据遍历 -->
                for (var index in skuIdDict.record) {
                  var localIdDict = skuIdDict.record[index];
                  localHtml += '<tr>'
                  localHtml += '<td class="text-primary span2 text-center"><span  style="width: 100px">' + localIdDict.keyword_name + '</span></td>'
                  // Web端
                  localHtml += '<td class="w150 text-center">'
                  if (!localIdDict.web_rank_text) {
                    localHtml += '<span class="btn btn-default btn-xs">O(∩_∩)O 要努力哦</span>'
                  } else {
                    localHtml += '<a href="javascript:void(0);" data-platform="web" target="_blank" class="pos-r label danger-bordered w115 J_compare" data-loc-id="' + localIdDict.keyword_id + '" data-loc-in-all="' + localIdDict.web_all_rank + '">'
                    localHtml += localIdDict.web_rank_text + '<i class="sq-8 bg-darkorange pos-a t-0 r-0" style="border-radius:50%;"></i></a>'
                    localHtml += $G.switchRankDiff(localIdDict.web_rank_diff);
                  }
                  // Wap端
                  localHtml += '<td class="w150 text-center">'
                  if (!localIdDict.wap_rank_text) {
                    localHtml += '<span class="btn btn-default btn-xs">O(∩_∩)O 还差一点</span>'
                  } else {
                    localHtml += '<a href="javascript:void(0);" data-platform="wap" target="_blank" class="pos-r label success-bordered w115 J_compare" data-loc-id="' + localIdDict.keyword_id + '" data-loc-in-all="' + localIdDict.wap_all_rank + '">'
                    localHtml += localIdDict.wap_rank_text + '<i class="sq-8 bg-darkorange pos-a t-0 r-0" style="border-radius:50%;"></i></a>'
                    localHtml += $G.switchRankDiff(localIdDict.wap_rank_diff);
                  }
                  // 微信端
                  localHtml += '<td class="w150 text-center">'
                  if (!localIdDict.wx_rank_text) {
                    localHtml += '<span class="btn btn-default btn-xs">O(∩_∩)O 就差一点</span>'
                  } else {
                    localHtml += '<a href="javascript:void(0);" data-platform="wx" target="_blank" class="pos-r label primary-bordered w115 J_compare" data-loc-id="' + localIdDict.keyword_id + '" data-loc-in-all="' + localIdDict.wx_all_rank + '">'
                    localHtml += localIdDict.wx_rank_text + '<i class="sq-8 bg-darkorange pos-a t-0 r-0" style="border-radius:50%;"></i></a>'
                    localHtml += $G.switchRankDiff(localIdDict.wx_rank_diff);
                  }
                  // QQ端
                  localHtml += '<td class="w150 text-center">'
                  if (!localIdDict.qq_rank_text) {
                    localHtml += '<span class="btn btn-default btn-xs">O(∩_∩)O 优化到底</span>'
                  } else {
                    localHtml += '<a href="javascript:void(0);" data-platform="qq" target="_blank" class="pos-r label warning-bordered w115 J_compare" data-loc-id="' + localIdDict.keyword_id + '" data-loc-in-all="' + localIdDict.qq_all_rank + '">'
                    localHtml += localIdDict.qq_rank_text + '<i class="sq-8 bg-darkorange pos-a t-0 r-0" style="border-radius:50%;"></i></a>'
                    localHtml += $G.switchRankDiff(localIdDict.qq_rank_diff);
                  }
                  localHtml += '<td class="text-center J_impression_265a9a84bfe5436b6bceb5974c5afe85">暂缓开通</td>'
                  localHtml += '<td class="text-center J_click_265a9a84bfe5436b6bceb5974c5afe85">暂缓开通</td>'
                  localHtml += '<td class="text-center J_payTradeAmt_265a9a84bfe5436b6bceb5974c5afe85">暂缓开通</td>'
                  localHtml += '<td class="span2 text-right">'
                  localHtml += '<a href="javascript:void(0);" class="btn btn-danger btn-xs J_addLocKeywordMonitor" style="margin-right: 2px" data-ware-id="' + skuIdDict.ware_id + '" data-keyword="' + localIdDict.keyword + '" data-hash="265a9a84bfe5436b6bceb5974c5afe85"><i class="fa fa-bell-o mr_5"></i>监控</a>'
                  localHtml += '<a href="javascript:void(0);" data-type="keyword" class="J_printLocKeywodChart btn btn-success btn-xs" data-sku-id="' + skuIdDict.sku_id + '" data-loc-id="' + localIdDict.keyword_id + '" data-keyword="' + localIdDict.keyword + '"><i class="fa fa-area-chart mr_5"></i>走势</a>'
                  localHtml += '</td> </tr>'
                }
                locSkuHtml += localHtml
                locSkuHtml += '</tbody> </table> </div> </div>'
              }
              ;
              if (!first) {
                $G.searchLocKeywordSkuList(obj.curr, locIds, obj.limit, callback);
              }
              $('#J_locKeywordSkuList').html(locSkuHtml);
              $('.J_locSkuListBarFixed').pin({padding: {top: 0}});
            }
          });
        });
        $G.skuCompare(ret['competeLocList']);
      } else {
        var tip = (locIds.length == 0) ? '无定位记录，请输入关键词，点击开始定位' : '关键词在指定的页码内未匹配到本店商品';
        return $('#J_locKeywordSkuList').html('<div class="jumbotron mt_10"><p class="lead text-center"><i class="fa fa-safari text-primary"></i> ' + tip + '<p></div>');
      }
    });
  },
  // 排名比较
  switchRankDiff: function (rank_diff) {
    var downIcon = '<i class="fa fa-long-arrow-down text-success fa-fw"></i>';
    var upIcon = '<i class="fa fa-long-arrow-up text-danger fa-fw"></i>';
    var rightIcon = '<i class="fa fa-long-arrow-right text-danger fa-fw"></i>';
    var diffHtml = '';
    switch (true) {
      case rank_diff > 0:
        diffHtml = '<span class="btn btn-xs">下降:' + downIcon + rank_diff + '</span></td>';
        break;
      case rank_diff < 0:
        diffHtml = '<span class="btn btn-xs">上升:' + upIcon + Math.abs(rank_diff) + '</span></td>';
        break;
      default:
        diffHtml = '<span class="btn btn-xs">持平:' + rightIcon + rank_diff + '</span></td>';
    }
    return diffHtml
  },
  // 竞品比较处理
  skuCompare: function (skuList) {
    if (_.isEmpty(skuList)) {
      return;
    }
    $('#J_locKeywordSkuList .J_compare').popover({
      title: "本店关键词排名与竞品排名比较",
      trigger: "hover",
      content: function () {
        var $t = $(this), locInAll = $t.data('locInAll'), platform = $t.data('platform'), locId = $t.data('locId');
        var tip = $G.formatPluckCompareSku(skuList, locId, locInAll, platform);
        return tip;
      },
      placement: "right",
      container: "body",
      animation: false,
      html: true,
      template: '<div class="popover span4" role="tooltip" style="max-width:300px;"><div class="arrow"></div><h3 class="popover-title ft_12"></h3><div class="popover-content ft_12"></div></div>'
    });
  },
  // 关键词竞品比较
  formatPluckCompareSku: function (skuList, locId, locInAll, platform) {
    var greater = [], less = [];
    $.each(skuList, function (i, sku) {
      if (sku.keyword_id != locId) {
        return;
      }
      var diffPos = 0;
      var posFormat = '';
      switch (true) {
        case platform == 'web':
          diffPos = sku['web_all_rank'] - locInAll;
          posFormat = sku['web_rank_text']
          break;
        case platform == 'wap':
          diffPos = sku['wap_all_rank'] - locInAll;
          posFormat = sku['wap_rank_text']
          break;
        case platform == 'wx':
          diffPos = sku['wx_all_rank'] - locInAll;
          posFormat = sku['wx_rank_text']
          break;
        case platform == 'qq':
          diffPos = sku['qq_all_rank'] - locInAll;
          posFormat = sku['qq_rank_text']
          break;
      }

      sku['difPos'] = diffPos;
      sku['posFormat'] = posFormat;
      (diffPos > 0) && less.push(sku);
      (diffPos < 0) && greater.push(sku);
    });
    if (greater.length == 0 && less.length == 0) {
      return '<div class="lead m-b-sm ft_16">该关键词未定位到竞品排名</div>';
    }

    var tip = '', formatSku = function (itemList) {
      var tpl = '<%_.each(itemList, function(sku, key){ %>\
							<div class="media m-b m-t-sm loc-result">\
								<div class="media-left">\
									<a target="_blank" href="<%= sku.itemUrl %>" style="margin-bottom:0px;">\
										<img src="<%= sku.imgUrl %>" class="header-avatar" style="width:45px;height:45px;">\
									</a>\
							 	</div>\
							 	<div class="media-body pt_5 ft_12">\
									<a href="<%= sku.itemUrl %>" class="fc-slate-gray truncate span3" target="_blank"><%= sku.title %></a>\
									<div class="text-muted m-t-sm">\
										<a class="label warning-bordered w115" style="padding:1px 3px;"><%= sku.posFormat %></a>\
										<% if(sku.difPos > 0){ %><span class="text-success">在你后 <%= Math.abs(sku.difPos) %> 名</span><% } else {%><span class="fc-red">在你前 <%= Math.abs(sku.difPos) %> 名</span><% }%>\
									</div>\
							 	</div>\
							</div><% });%>';
      return _.template(tpl)({
        'itemList': itemList
      });
    };

    if (greater.length > 0) {
      tip += '<p class="lead text-danger m-b-sm ft_14">以下  <b class="ft_16">' + greater.length + '</b> 个竞品在你排名之前</p>';
      tip += formatSku(greater);
    }
    if (less.length > 0) {
      tip += '<p class="lead text-success m-b-sm ft_14">以下 <b class="ft_14">' + less.length + '</b> 个竞品在你排名之后</p>';
      tip += formatSku(less);
    }

    return tip;
  },
  // 定位历史请求
  historyKeywords: function (target, p, callback) {
    var $target = $('#' + target);
    $target.searchLoad({'min-height': '200px'});
    $.ajax({
      url: Urls.historyKeywords,
      data: {"page": p},
      method: 'get',
      dataType: 'json'
    }).always(function () {
      $target.searchLoad('hide')
    }).done(function (ret) {
      var resultsList = ret.results;
      if (resultsList.length) {
        var keywordHtml = '';
        for (var index in resultsList) {
          var infoDict = resultsList[index];
          var data_local_dict = {
            keywordCnt: infoDict.count,
            psortName: infoDict.sort,
            gmtLoc: infoDict.create_time
          };
          keywordHtml += '<div class="item-list J_locKeywordNode"><i class="fa fa-clock-o fa-fw icon"></i>'
          keywordHtml += '<div class="inline-box no-padding ws-normal ft_12">'
          // <!-- 关键词组：手机,电脑,台式机 -->
          keywordHtml += '<span class="fc_333 mr_5 inline-box no-padding ws-normal text-left" style="max-width:300px;">' + infoDict.keywords + '</span>'
          // <!-- 排序名称：[综合] -->
          keywordHtml += '<span class="nline-box no-padding fc-blue">[' + infoDict.sort + '] </span>'
          // <!-- 抓取时间：2019-01-22 20:46:20 -->
          keywordHtml += '<span class="nline-box no-padding">' + infoDict.create_time + '</span></div>'
          // <!-- 历史数据渲染到DOM标签中 -->
          keywordHtml += '<div style="position:absolute;right:5px; top:5px">'
          // <!-- 查看操作 -->
          keywordHtml += '<a href="javascript:void(0);"'
          keywordHtml += "data-task-list='" + JSON.stringify(infoDict.record) + "' "
          keywordHtml += "data-loc-info='" + JSON.stringify(data_local_dict) + "' "
          keywordHtml += 'class="btn btn-xs btn-primary J_getLocKeywordHistory" style="margin-right:5px;">查看</a>'
          // <!-- 定位操作 -->
          keywordHtml += '<a href="javascript:void(0);"'
          keywordHtml += "data-task-list='" + JSON.stringify(infoDict.record) + "' "
          keywordHtml += "data-loc-info='" + JSON.stringify(data_local_dict) + "' "
          keywordHtml += 'class="btn btn-xs btn-warning J_addKeywordToBox" style="margin-right:5px;"><i class="fa fa-map-marker"></i> 定位</a>'
          // <!-- 添加操作 -->
          keywordHtml += '<a href="javascript:void(0);"'
          keywordHtml += "data-task-list='" + JSON.stringify(infoDict.record) + "' "
          keywordHtml += "data-loc-info='" + JSON.stringify(data_local_dict) + "' "
          keywordHtml += 'class="btn btn-xs btn-info J_appendKeywordToBox" style="margin-right:5px;"><i class="fa fa-plus"></i> 添加</a>'
          // <!-- 删除操作 -->
          keywordHtml += '<a href="javascript:void(0);" data-group-id="' + infoDict.id + '"'
          keywordHtml += 'class="btn btn-xs btn-danger J_delLocKeywords">删除</a>'
          keywordHtml += '</div></div></div>'
        }
        $target.empty().html(keywordHtml);
      }
      if ($.type(callback) == 'function') {
        callback(ret);
      }
    });
  },
  // 删除定位历史
  recommendKeywords: function (target, p, callback) {
    var type = 'traffic';
    target = target || 'J_locKeywordHistory';
    switch (target) {
      case 'J_locKeywordHistory':
        type = 'history';
        break;
      case 'J_trafficKeywords':
        type = 'traffic';
        break;
      case 'J_fatoriveKeyword':
        type = 'fatorive';
        break;
    }
    var $target = $('#' + target);
    $target.searchLoad({'min-height': '200px'});
    $.ajax({
      url: Urls.recommendKeywords,
      data: {"type": type, "page": p},
      method: 'get',
      dataType: 'json'
    }).always(function () {
      $target.searchLoad('hide')
    }).done(function (ret) {
      if (ret.result == 'success') {
        $target.empty().html(ret.keywordHtml);
      }
      if ($.type(callback) == 'function') {
        callback(ret);
      }
    });
  },
  // 搜索参数映射关系key，value
  getValMap: function ($t) {
    var valueMap = {};
    if ($t.length == 0) {
      return valueMap;
    }
    $.each($t.serializeArray(), function (i, field) {
      valueMap[field.name] = field.value;
    });
    return valueMap;
  },
  // 定位历史删除操作
  deleteLocKeywordGroup: function (groupId, callback) {
    var layerId = layer.load('正在删除历史');
    $.ajax({
      url: Urls.delKeywordHistoryGroup,
      data: {"group_id": groupId, "is_del": true},
      method: 'post',
      dataType: 'json'
    }).always(function () {
      layer.close(layerId);
    }).done(function (ret) {
      if ($.type(callback) == 'function') {
        callback(ret);
      }
    });
  }
};

$(function () {
  // 调用功能函数
  initOptions.init();
  $('[data-toggle="tooltip"], .J_tooltip').tooltip();
  $('.J_bulidSimpleSkus').slimScroll({
    height: '520px',
    railVisible: true
  });
});
