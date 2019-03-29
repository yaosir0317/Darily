var JX = JX || {};
var Host = window.location.protocol + '//' + window.location.host + '/';
var locHostMap = locHostMap || [Host];

// 自执行函数
+function ($) {
  var timeoutId, checkTryTimes = 0, breatheTimes = 4, date = new Date, curHour = date.getHours();
  var Urls = {
    // TAB下拉框中的历史数据请求处理
    recommendKeywords: Host + 'data/loc/recommend_keywords',
    // TAB下拉框中获取历史的组ID
    getLocKeywordHistoryGroup: Host + 'data/loc/getLocKeywordHistoryGroup',
    processKeywordLocData: Host + 'data/loc/process_keyword_loc_data',
    // TODO 审核关键词查询是否完成  已经添加
    checkLocKeywords: Host + 'data/loc/check_loc_keywords',
    // 获取搜索关键词SKU列表
    searchLocKeywordSkuList: Host + 'data/loc/searchLocKeywordSkuList',
    // 获取搜索关键词竞品SKU列表
    searchLocKeywordCompeteSkuList: Host + 'data/loc/searchLocKeywordCompeteSkuList',
    // 获取搜索关键词推广SKU列表
    searchLocKeywordPromoSkuList: Host + 'data/loc/searchLocKeywordPromoSkuList',
    // 关键词和类目图表展示
    locKeywordAndCateSkuChart: Host + 'data/loc/loc_keyword_and_cate_sku_chart',
    locKeywordCateHitSkuChart: Host + 'data/loc/loc_keyword_cate_hit_sku_chart',
    // 关键词和类目竞品图表展示
    locKeywordOrCateCompeteSkuChart: Host + 'data/loc/locKeywordOrCateCompeteSkuChart',
    // TODO 添加关键词组查询--一键查排名  已经添加
    addKeywordGroup: Host + 'data/loc/addKeywordGroup',
    // 添加关键词监控按钮
    addLocKeywordMonitor: Host + 'data/loc/addLocKeywordMonitor',
    // 取消关键词查询任务
    cancelLocKeyword: Host + 'data/loc/cancelLocKeyword',
    // 搜索有效关键词查询列表
    searchSkuKeywordEffect: Host + 'data/loc/searchSkuKeywordEffect',
    // 添加推广SKU到竞品
    addPromoSkuToCompete: Host + 'data/compete/add_compete_sku',
    // 删除关键词查询历史
    delLocKeywordHistoryGroup: Host + 'data/loc/delLocKeywordHistoryGroup',
    // 获取排名变化信息和展示数据
    getPrevTopLocKeywordSkuMap: Host + 'data/loc/getPrevTopLocKeywordSkuMap',
    // 统计关键词下推广商品的数量
    countLocKeywordPromoSku: Host + 'data/loc/countLocKeywordPromoSku'
  }
    , Uris = {
    // 添加关键词
    addLocKeyword: '/data/loc/add_loc_keyword',
    // 开始抓取Web关键词信息
    startCrawlKeyword: '/data/loc/start_crawl_keyword',
    // 开始抓取移动端关键词信息
    startCrawlKeywordM: '/data/loc/start_crawl_keyword_m',
    // 开始抓取app端关键词信息
    startCrawlKeywordApp: '/data/loc/startCrawlKeywordApp'

  }
    , $G = {}
    , keywordBox = []
    , taskMap = []
    , locSkuList = []
    , locCompeteSkuList = []
    , $chart = JX.locChart
    , locRunning = false;
  var v3 = function (name) {
    this.name = name;
  };
  var locKeyword = {
    // 重置搜索框-初始化操作
    resetBox: function () {
      keywordBox = [],
        taskMap = [];
      $('.J_queryKeywordList').find('.J_keyword').remove();
      $('#J_locKeywordTaskList').find('.J_locKeywordLabel').remove();
    },
    // 添加关键词到搜索框
    addKeywordsToBox: function (keyword) {
      var keyword = $.trim(keyword)
        , keyword = keyword.toString();
      // 用户未操作的情况或用户重复输入关键词
      if (_.isEmpty(keyword) || ($.inArray(keyword, keywordBox) !== -1)) {
        return false;
      }
      // 最多关键词数量判断
      var dt = new Date(), curH = dt.getHours();
      //var maxKeyword = ((curH >= 9) && (curH <= 11)) ? 4 : 8;
      var maxKeyword = 12;
      if (keywordBox.length == maxKeyword) {
        layer.alert("一次最多只能输入" + maxKeyword + "个关键词");
        return false;
      }
      keywordBox.push(keyword);
      this.buidHtml();
    },
    // 删除输入关键词样式x
    removeKeywordsFromBox: function (keyword) {
      var keyword = $.trim(keyword)
        , keyword = keyword.toString();
      var idx = $.inArray(keyword, keywordBox);
      if (_.isEmpty(keyword) || (idx === -1)) {
        return false;
      }
      keywordBox.splice(idx, 1);
      this.buidHtml();
    },
    // 构造输入的关键词样式
    buidHtml: function () {
      var qhtml = '';
      if (keywordBox.length == 0) {
        $('.J_queryKeywordList').html('');
      }
      keywordBox.forEach(function (tmpKeyword) {
        if (_.isEmpty(tmpKeyword)) {
          return;
        }
        // 前端js模板变量渲染DOM，不需要Django传输数据
        var keywordHtml = _.template(
          '<span class="tag label label-info J_keyword" data-keyword="<%= locKeyword %>"><%= locKeyword %>' +
          '<span data-role="remove" data-keyword="<%= locKeyword %>"></span>' +
          '</span>'
        )({
          locKeyword: tmpKeyword
        });
        qhtml += keywordHtml
      });
      $('.J_queryKeywordList').empty().html(qhtml);
    },
    // 构建搜索关键词显示label，前端template js DOM结构数据
    buildLocKeywordLabel: function (locId, keyword, process, pcMatch, mMatch, appMatch, status) {
      var tpl = '' +
        '<div class="col-xs-3 p-x J_locKeywordLabel m-b" id="J_locKeywordTask_<%= locId %>" data-loc-id="<%= locId %>">'
        + '  <div class="databox databox-shadowed animated zoomIn m-b-0">'
        + '    <div class="databox-left <%= (status == "success") ? "bg-green" : (status == "process" ? "bg-azure" : "bg-gray") %>">'
        + '      <div class="databox-piechart <%= (status == "process") ? "activity" : "" %>"></div>'
        + '      <div class="databox-process J_process"><%= process %>%</div>'
        + '    </div>'
        + '    <div class="databox-right">'
        + '      <span class="databox-number"><%= keyword %></span>'
        + '      <div class="databox-text darkgray truncate">' +
        '           PC:<span class="J_pc fc-red"><%= pcMatch %></span>' +
        '           个&nbsp;安卓:<span class="J_app fc-red"><%= appMatch %></span>' +
        '           个&nbsp;微信:<span class="J_m fc-red"><%= mMatch %></span>' +
        '           个<span class="J_promo loc-promo-tip m-l-sm" style="display:noen;"></span>' +
        '        </div>'
        + '      <div class="databox-state J_state" style="display:none;">' +
        '           <i class="fa fa-check-circle fa-lg"></i>' +
        '        </div>'
        // TODO 取消操作按钮
        + '      <a href="javascript:void(0);"  style="<%= (status == "process") ? "display:block;" : "display:none;"%>" class="databox-state J_cancelLocSearch fc-red" data-loc-id="<%= locId %>">' +
        '          <i class="fa fa-undo"></i>' +
        '        </a>'
        + '    </div>'
        + '  </div>'
        + '</div>';
      // 变量替换渲染，返回数据渲染后的DOM对象
      var compiled = _.template(tpl)({
        'locId': locId,
        'keyword': keyword,
        'process': process > 0 ? process : 0,
        'pcMatch': pcMatch >= 0 ? pcMatch : '--',
        'mMatch': mMatch >= 0 ? mMatch : '--',
        'appMatch': appMatch >= 0 ? appMatch : '--',
        'status': status
      });
      // DOM对象追加到 #J_locKeywordTaskList div标签下
      $('#J_locKeywordTaskList').append(compiled);
    },
    // 查询后的统计信息
    buildHistoryLable: function (keywordCnt, psortName, gmtLoc) {
      var paramHtml = _.template('共定位<span class="fc-red lead ft_16"> <%= keywordCnt %> </span>个关键词，排序：<span class="fc-red lead ft_16"> <%= psortName %> </span>，定位时间：<span class="fc-red lead ft_16"> <%= gmtLoc %> </span></span>')({
        'keywordCnt': keywordCnt,
        'psortName': psortName,
        'gmtLoc': gmtLoc
      });
      $('#J_locHistorySetting').empty().html(paramHtml).show();
    }
  };
  v3.prototype = {
    init: function () {
      $G = v3.prototype;
      $G.searchbarInit();
      $G.chartEvent();
      $G.historyEvent();
      $G.initHistory();
    },
    // 初始化搜索操作
    searchbarInit: function () {
      // 下拉菜单点击默认事件阻止
      $('.dropdown > .dropdown-menu').on('click', function (e) {
        e.stopPropagation();
      });
      // 点击搜索输入框，光标聚焦到输入框内部
      $('.J_searchbarMain').on('click', function () {
        $('#J_enterKeyword').focus();
      });

      /* recommend keyword */
      // 光标聚焦时，查找最近的tags-input，添加class：focus
      $('#J_enterKeyword').on('focusin', function () {
        $(this).closest('.bts-tagsinput').addClass('focus');
      });
      // 光标失去焦点时，清除class：foucus
      $('#J_enterKeyword').on('focusout', function () {
        $(this).closest('.bts-tagsinput').removeClass('focus');
      });
      // 下拉显示框，显示tab信息
      $('.J_searchbarMain').on('shown.bs.dropdown', function () {
        var target = $('.J_recommendKeywords > li.active > a').data('tab');
        // 请求数据，翻页
        $G.recommendKeywords(target, 1);
      });
      $('.J_recommendKeywords > li a').on('click', function (e) {
        e.preventDefault();
        $(this).tab('show');
      });
      $('.J_recommendKeywords > li a').on('shown.tab.bs', function () {
        var $this = $(this)
          , target = $this.data('tab');
        $G.recommendKeywords(target, 1);
      });


      $('.J_recommendKeywordPanel').on('click', '.zc-pagination ul > li > a', function (e) {
        e.preventDefault();
        var target = $('.J_recommendKeywords > li.active a').data('tab');
        $G.recommendKeywords(target, $(this).data('pageNo'));
      });


      // 搜索参数设置
      $('.J_setSearchParam').on('click', function () {
        var setting = $G.getValMap($('#J_locSetting input'));
        var paramHtml = _.template('<span class="fc-red"><%= psort %></span>，PC<span class="fc-red"><%= pcMaxPage %></span>页，移动<span class="fc-red"><%= mMaxPage %></span>页')({
          psort: $('#J_locSetting [name="psort"]:checked').data('name'),
          pcMaxPage: setting['maxPage'],
          mMaxPage: setting['maxPageM']
        });
        // 渲染页面
        $('.J_searchParam').html(paramHtml);
        $('#J_locSetting').parent('.dropdown').removeClass('open');
      });

      // tab中的添加
      $('.J_recommendKeywordPanel').on('click', '.J_recommendKeywordLoc', function (e) {
        e.preventDefault();
        locKeyword.addKeywordsToBox($(this).data('keyword'));
      });
      // tab中的定位
      $('.J_recommendKeywordPanel').on('click', '.J_addKeywordToBox', function (e) {
        e.preventDefault();
        var taskList = $(this).data('taskList');
        if (taskList.length == 0) {
          return false;
        }
        //locKeyword.resetBox();
        keywordBox = [],
          taskMap = [];
        $('.J_queryKeywordList').find('.J_keyword').remove();
        // 添加定位关键词到搜索框
        $.each(taskList, function (i, task) {
          locKeyword.addKeywordsToBox(task['keyword']);
        });
      });
      // tab中的添加
      $('.J_recommendKeywordPanel').on('click', '.J_appendKeywordToBox', function (e) {
        e.preventDefault();
        var taskList = $(this).data('taskList');
        if (taskList.length == 0) {
          return false;
        }
        $.each(taskList, function (i, task) {
          locKeyword.addKeywordsToBox(task['keyword']);
        });
      });
      // tab中的删除
      $('.J_recommendKeywordPanel').on('click', '.J_delLocKeywords', function () {
        var groupId = $(this).data('groupId');
        $G.deleteLocKeywordGroup(groupId, function (ret) {
          if (ret.result == 'success') {
            $G.recommendKeywords('J_locKeywordHistory', 1);
          } else {
            var reason = isEmpty(ret['reason']) ? '删除定位历史失败' : ret['reason'];
            layer.alert(reason);
          }
        });
      });

      // 删除搜索框中的关键词
      $('.J_queryKeywordList').on('click', '[data-role="remove"]', function () {
        locKeyword.removeKeywordsFromBox($(this).data('keyword'));
      });

      // 回车添加关键词
      $('#J_enterKeyword').on('keydown', function (e) {
        var keyword = $(this).val();
        // 回车键操作
        if (e.keyCode == 13) {
          if (_.isEmpty(keyword)) {
            layer.alert("请先输入关键词，然后再回车完成，可添加多个关键词");
            return false;
          }
          locKeyword.addKeywordsToBox(keyword);
          $(this).val('');
        }
        // 删除键操作
        if (e.keyCode == 8 && _.isEmpty(keyword)) {
          var $kList = $(this).prev('.J_queryKeywordList');
          var $k = $kList.find('>.J_keyword:last')
            , keyword = $k.data('keyword');
          locKeyword.removeKeywordsFromBox(keyword),
            $k.remove();
        }
      });
      // 一键查排名按钮操作
      $('#J_startLocKeyword').on('click', function () {
        var enterKeyword = $('#J_enterKeyword').val()
          , enterKeywords = [];
        !_.isEmpty(enterKeyword) && (enterKeywords = enterKeyword.split(/,|，/ig));
        enterKeywords.length && enterKeywords.forEach(function (tmpKeyword) {
          locKeyword.addKeywordsToBox(tmpKeyword);
        });
        $('#J_enterKeyword').val('');
        // 启动
        $G.startLocKoywordBox();
      });
      if (keywordBox.length == 0 && $('.J_queryKeywordList .J_keyword').length > 0) {
        $('.J_queryKeywordList .J_keyword').each(function (i) {
          locKeyword.addKeywordsToBox($(this).data('keyword'));
        });
      }
      $('#J_locKeywordTaskList').on('click', '.J_cancelLocSearch', $G.cancelLocKeyword);
    },

    chartEvent: function () {
      $('#J_locKeywordSkuList').on('click', '.J_printLocKeywodChart', function () {
        var locId = $(this).data('locId')
          , skuId = $(this).data('skuId')
          , keyword = $(this).data('keyword');
        var titleHtml = _.template('<i class="fa fa-area-chart mr_5"></i>关键词【<b class="text-danger"><%= keyword %></b>】在京东搜索页面的商品排名走势')({
          'keyword': keyword
        });

        $('#J_locKeywordModal').find('li.J_defalutChartTab').addClass('hidden');
        $('#J_locKeywordModal').find('li.J_compareTab > a').tab('show');
        $('#J_locKeywordModal .modal-title').html(titleHtml);
        $('#J_locKeywordModal').modal();
        $('#J_locKeywordModal').find('li.J_compareTab, li.J_mChartTab').removeClass('hidden');
        (locSkuList.length > 0) && $G.format.bulidSimpleSkus(locSkuList, skuId, locId);

        var skuTitle = $('#J_locKeywordModal').find('.J_printLocKeywodChart[data-sku-id="' + skuId + '"]').data('title');
        $('.J_curHistorySkuTitle').html(skuTitle).show();
        $G.printKeywordChart(skuId, locId);
      });
      $('#J_locKeywordModal').on('click', '.J_printLocKeywodChart', function () {
        var locId = $(this).data('locId')
          , skuId = $(this).data('skuId');
        $('#J_locKeywordModal').find('.J_printLocKeywodChart').removeClass("active");
        $(this).addClass("active");

        var skuTitle = $(this).data('title');
        $('.J_curHistorySkuTitle').html(skuTitle);
        $G.printKeywordChart(skuId, locId);
      });

      $('.J_cpIdxSelect').on('click', function () {
        var idx = $(this).find('a').data('idx')
          , idxName = $(this).data('title');
        $('.J_cpIdxSelect').removeClass('active');
        $(this).addClass('active');
        $('.J_selectIndex').find('.J_idxName').empty().html(idxName);
        $G.format.formatKeywordCompareChart('#J_keywordLocCompareCharts', idx, idxName);
      });

      $('#J_locKeywordCompeteSkuList').on('click', '.J_printLocCompeteChart', function () {
        var locId = $(this).data('locId')
          , skuId = $(this).data('skuId')
          , competeSkuId = $(this).data('competeSkuId');
        $('#J_locKeywordModal').find('li.J_defalutChartTab').removeClass('hidden');
        $('#J_locKeywordModal').find('li.J_compareTab, li.J_mChartTab, li.J_appChartTab').addClass('hidden');
        $('#J_locKeywordModal').find('li.J_defalutChartTab > a').tab('show');
        $('.J_curHistorySkuTitle').hide();
        $('#J_locKeywordModal').modal();
        (locCompeteSkuList.length > 0) && $G.format.bulidSimpleCompeteSkus(locCompeteSkuList, skuId, locId);
        $G.printKeywordCompeteSkuChart(skuId, locId, competeSkuId);
      });
      $('#J_locKeywordModal').on('click', '.J_printLocCompeteChart', function () {
        var locId = $(this).data('locId')
          , skuId = $(this).data('skuId')
          , competeSkuId = $(this).data('competeSkuId');
        $('#J_locKeywordModal').find('.J_printLocCompeteChart').removeClass("active");
        $(this).addClass("active");
        $G.printKeywordCompeteSkuChart(skuId, locId, competeSkuId);
      });
      $('#J_locKeywordSkuList').on('click', '.J_addLocKeywordMonitor', $G.addLocKeywordMonitor);
    },

    historyEvent: function () {
      // 本店商品，竞品，推广商品
      $('.J_locSkuListContent').on('click', '.J_keywordSkuPagin li > a, .J_competeKeywordSkuPagin li > a, .J_promoKeywordSkuPagin li > a', function (e) {
        e.preventDefault();
        var target = $("#J_curLocTarget").val();
        $G.getLocResultData(target, $(this).data('pageNo'));
      });
      // 本店商品，竞品，推广商品 TAB
      $('.J_btnGroupTab li > a').on('click', function () {
        var target = $(this).data('goal');
        $('#J_curLocTarget').val(target),
          $('#J_locFilterKeyword').val('');
        $G.getLocResultData(target, 1);
      });
      // 推广商品中的：添加到竞品
      $('.J_locSkuListContent').on('click', '.J_addPromoSkuToCompete', function () {
        var skuId = $(this).data('skuId');
        $G.addPromoSkuToCompete(skuId);
      });
      // 关键词搜索筛选列表
      $('.J_locFilterKeywordBtn').on('click', function () {
        var target = $('#J_curLocTarget').val();
        $G.getLocResultData(target, 1);
      });

      /** loc history **/
      $('.J_locHistoryDp').on('show.bs.dropdown', function () {
        $G.getLocHistory();
      });

      $('#J_locHistory').on('click', '.pagination li a', function (e) {
        e.preventDefault();
        $G.getLocHistory($(this).data('pageNo'));
      });

      // 历史tab中的查看按钮
      $('.J_recommendKeywordPanel').on('click', '.J_getLocKeywordHistory', function (e) {
        e.preventDefault();
        var taskList = $(this).data('taskList')
          , locInfo = $(this).data('locInfo');
        if (taskList.length > 0) {
          historyTaskList = taskList;
          $G.initHistory();

          locKeyword.buildHistoryLable(locInfo['keywordCnt'], locInfo['psortName'], locInfo['gmtLoc']);
          $('.J_searchbarMain').removeClass('open');
        }
      });
      //  历史tab中的删除按钮
      $('#J_locHistory').on('click', '.J_delLocKeywords', function () {
        var groupId = $(this).data('groupId');
        $G.deleteLocKeywordGroup(groupId, function (ret) {
          if (ret.result == 'success') {
            $G.getLocHistory();
          } else {
            var reason = isEmpty(ret['reason']) ? '删除定位历史失败' : ret['reason'];
            layer.alert(reason);
          }
        });
      });
      // 关键词label，指定查询对应的排名信息
      $('#J_locKeywordTaskList').on('click', '.J_locKeywordLabel', function () {
        var $t = $(this)
          , $r = $t.find('.databox-right')
          , $box = $t.find('.databox')
          , locId = $t.data('locId');
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

        var target = $("#J_curLocTarget").val();
        $G.getLocResultData(target, 1);
      });
    },

    // 初始化历史查询信息
    initHistory: function () {
      if (historyTaskList.length > 0) {
        locKeyword.resetBox();
        var target = $('#J_curLocTarget').val();
        // TODO 历史关键词查询进度
        for (var i in historyTaskList) {
          var task = historyTaskList[i];
          var process = (task['process'] > 100) ? 100 : task['process']
            , processM = (task['process_m'] > 100) ? 100 : task['process_m']
            , processApp = (task['process_app'] > 100) ? 100 : task['process_app']
          var estimate = parseInt((process + processM + processApp) / 3);

          taskMap.push({
            'locId': task['locId'],
            'keyword': task['keyword'],
            'process': estimate,
            'tryTimes': 0,
            'status': task['taskStatus']
          });
          // TODO 参数需要多加QQ，变量名称有改动
          locKeyword.buildLocKeywordLabel(task['locId'], task['keyword'], estimate, task['hitNum'], task['hitNumM'], task['hitNumApp'], task['taskStatus']);
        }
        var locIds = $G.getRunningLocIds();
        if (locIds.length == 0) {
          return false;
        }

        locRunning = true;
        $G.checkLocTaskFinish(function () {
          $G.getLocResultData(target, 1, function (ret) {
            $G.revertAction();
          }),
            $G.tooltipBox(),
            $G.tipPromoLocKeyword();
        });
      }
    },

    // 关键词Label运行
    startLocKoywordBox: function () {
      if (keywordBox.length == 0) {
        layer.alert("请先输入关键词");
        return false;
      }
      if (locRunning == true) {
        layer.alert("定位正在运行，请完成之后操作");
        return false;
      }

      var psort = $('#J_locSetting input[name="psort"]:checked').val();
      var iid = layer.load("正在初始化关键词");
      // 排序，页码参数
      var locParams = $G.getValMap($('#J_locSetting input'));
      $.ajax({
        url: Urls.addKeywordGroup,
        data: {
          "keywordGroup": keywordBox,
          'locParams': locParams
        },
        method: 'post',
        dataType: 'json'
      }).always(function () {
        layer.close(iid);
      }).then(function (ret) {
        // ZcLog.log("Add Keywords To Group And AddRet Is :");
        // ZcLog.log(ret);
        if (ret['result'] == 'fail') {
          layer.alert(ret['reason']);
          return false;
        }

        locRunning = true,
          breatheTimes = 0;
        // 搜索查询后的搜索框处理情况
        $('#J_locKeywordTaskList').html('');
        $('#J_curLocPsortName').val(ret['psortName']);
        $('#J_curGtmLoc').val(ret['gmtLoc']);
        $('#J_curKeywordCnt').val(ret['keywordCnt']);
        $('#J_startLocKeyword').addClass('disabled').prop('disablde', true).html('<i class="fa fa-spinner fa-pulse fa-fw mr_5"></i>定位中 ...');

        var locInfo = ret['locInfo'];
        taskMap = [];
        for (var i in locInfo) {
          var loc = locInfo[i];
          locKeyword.buildLocKeywordLabel(loc['locId'], loc['keyword'], 0, 0, 0, 0, loc['status']);
          taskMap.push({
            'locId': loc['locId'],
            'keyword': loc['keyword'],
            'process': 0,
            'tryTimes': 0,
            'status': loc['status']
          });
        }
        // ZcLog.log("Start checkLocTaskFinish And TaskMap is");
        // ZcLog.log(taskMap);
        // 检查任务是否完成
        $G.checkLocTaskFinish(function () {
          // 获取运行任务ID
          var locIds = $G.getRunningLocIds();
          var target = $("#J_curLocTarget").val();
          // ZcLog.log('callback success');
          // 获取数据结果
          $G.getLocResultData(target, 1, function (ret) {
            var keywordCnt = $('#J_curKeywordCnt').val()
              , psortName = $('#J_curLocPsortName').val()
              , gmtLoc = $('#J_curGtmLoc').val();
            locKeyword.buildHistoryLable(keywordCnt, psortName, gmtLoc);
          }),
            $G.tooltipBox(),
            $G.tipPromoLocKeyword();
          $G.revertAction();
        });
      });
    },


    tooltipBox: function () {
      var $box = $('.J_locKeywordLabel');
      $box.find('.databox').addClass('pointer'),
        $box.tooltip({
          title: "单击关键词标签，可单独查看该关键词的定位结果。"
        });
    },
    tipPromoLocKeyword: function () {
      var locIds = $G.getRunningLocIds();
      $.ajax({
        url: Urls.countLocKeywordPromoSku,
        data: {
          "locIds": locIds
        },
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

    // 检测查询任务进度
    checkLocTaskFinish: function (callback) {
      var locIds = $G.getRunningLocIds();
      // ZcLog.log('checkLocTaskFinish Running LocIds And Running : ' + locRunning);
      // ZcLog.log(locIds);

      if (locRunning == false) {
        return false;
      }

      if ((taskMap.length > 0) && (locIds.length == 0)) {
        $G.revertAction();
      }
      // 定时巡检任务状态
      if ((locRunning == true) && (locIds.length == 0)) {
        timeoutId = setTimeout((function (callback) {
            return function () {
              $G.checkLocTaskFinish(callback);
            }
              ;
          }
        )(callback), 10000);
        return false;
      }

      $.ajax({
        url: Urls.checkLocKeywords,
        data: {
          "locIds": locIds
        },
        method: 'post',
        dataType: 'json'
      }).done(function (locRets) {
        breatheTimes++;
        // ZcLog.log('breatheTimes : ' + breatheTimes + ' CurHour : ' + curHour);
        var needWait = false;
        if ((curHour >= 9) && (curHour <= 10)) {
          needWait = (breatheTimes < 4) ? true : false;
        }

        var allTaskIsEnd = true
          , maxTimeout = (locIds.length * 80);
        $.each(locRets, function (locId, ret) {
          // ZcLog.log('=== Start Process LocId ' + locId + ' ===');
          // ZcLog.log(ret);
          if ($.inArray(ret['status'], ['cancel', 'fail', 'delete']) != -1) {
            ZcLog.log('Status Id ' + ret['status'] + ' LocId ' + locId);
            if (ret['status'] == 'fail') {
              var $dom = $('#J_locKeywordTaskList').find('#J_locKeywordTask_' + locId);
              $dom.find('.databox-left.bg-azure').removeClass('bg-azure').addClass('bg-gray');
              $dom.find('.activity').removeClass('activity');
            }
            return;
          }

          var curLocId = locId;
          var process = ret['process'] > 100 ? 100 : ret['process'];
          var processM = ret['process_m'] > 100 ? 100 : ret['process_m'];
          var processApp = ret['process_app'] > 100 ? 100 : ret['process_app'];
          var estimate = parseInt((process + processM + processApp) / 3);
          // ZcLog.log('estimate ' + estimate);
          if (estimate == 0) {
            checkTryTimes++
            if (checkTryTimes > maxTimeout) {
              // ZcLog.log('CheckTimeOut checkTryTimes: ' + checkTryTimes);
              $G.revertAction();
              layer.alert('定位超时，请重试或联系客服。');
              return false;
            }
          }

          var $dom = $('#J_locKeywordTaskList').find('#J_locKeywordTask_' + curLocId);
          // ZcLog.log('Get $dom Length: ' + $dom.length);
          if ($dom.length > 0) {
            if (needWait && estimate >= 100) {
              estimate = 99;
            }
            $dom.find('.J_process').html(estimate + '%');
            $dom.find('.J_pc').html(ret['hit_sku_num']);
            $dom.find('.J_m').html(ret['hit_sku_num_m']);
            $dom.find('.J_app').html(ret['hit_sku_num_app']);
            if (estimate >= 100) {
              ZcLog.log('Dom End Process estimate: ' + estimate);
              $G.endLocKeywordLable(locId);
            }
          }
          if ((ret['status'] != 'success') || (ret['status_m'] != 'success') || (ret['status_app'] != 'success')) {
            // ZcLog.log('allTaskIsEnd is not End');
            allTaskIsEnd = false;
          }
          // ZcLog.log('End Checked Bye !');
        })

        if ((allTaskIsEnd == true) && !needWait) {
          // ZcLog.log('allTaskIsEnd is End');
          if ($.type(callback) == 'function') {
            // ZcLog.log('Start Callback Function');
            callback(locRets);
          }
          return false;
        }

        timeoutId = setTimeout((function (callback) {
            return function () {
              $G.checkLocTaskFinish(callback);
            }
              ;
          }
        )(callback), 3000);
      });
    },

    cancelLocKeyword: function () {
      var $this = $(this)
        , locId = $this.data('locId');
      if (locId <= 0) {
        layer.alert("参数错误");
        return false;
      }

      layer.confirm("您确定要取消定位该关键词吗？", function () {
        var iid = layer.load("正在取消一项定位任务 ...")
        $.ajax({
          url: Urls.cancelLocKeyword,
          data: {
            "locId": locId
          },
          method: 'post',
          dataType: 'json'
        }).always(function () {
          layer.close(iid);
        }).done(function (ret) {
          if (ret.result == 'success') {
            $.each(taskMap, function (i, v) {
              if (v.locId == locId) {
                taskMap[i]['status'] = 'cancel';
              }
            });
            ZcLog.log(taskMap);
            var $dom = $('#J_locKeywordTaskList').find('#J_locKeywordTask_' + locId);
            $dom.find('.databox-left.bg-azure').removeClass('bg-azure').addClass('bg-gray');
            $dom.find('.activity').removeClass('activity');
          } else {
            layer.alert("定位任务取消失败");
          }
          //$("#J_curLocId").val('');
        });
      });
    },

    revertAction: function () {
      clearTimeout(timeoutId);
      checkTryTimes = 0;
      locRunning = false;
      ZcLog.log($('#J_startLocKeyword').length);
      $('#J_startLocKeyword').removeClass('disabled').prop('disabled', false).html('一键查排名');
    },

    endLocKeywordLable: function (locId) {
      var $dom = $('#J_locKeywordTaskList').find('#J_locKeywordTask_' + locId);
      $dom.find('.databox-piechart.activity').removeClass('activity');
      $dom.find('.databox-left.bg-azure').removeClass('bg-azure').addClass('bg-green');
      //$dom.find('.J_state').show();
      $dom.find('.J_cancelLocSearch').hide();

      $.each(taskMap, function (i, v) {
        if (v['locId'] == locId) {
          v['status'] = 'success';
          return false;
        }
      });
    },
    getRunningLocIds: function () {
      var locIds = [];
      $.each(taskMap, function (i, v) {
        if (_.has(v, 'status') && $.inArray(v['status'], ['process', 'success']) != -1) {
          locIds.push(v['locId']);
        }
      })

      return locIds;
    },

    getLocResultData: function (target, page, callback) {
      var page = page > 0 ? page : 1;
      var locIds = $G.getRunningLocIds()
        , selectedLocIds = [];
      $.each($('.J_locKeywordLabel'), function () {
        var locId = $(this).data('locId');
        if (locId > 0 && ($(this).find('.databox.active').length > 0)) {
          selectedLocIds.push(locId);
        }
      });
      if (selectedLocIds.length == 0) {
        selectedLocIds = locIds;
      }
      switch (target) {
        case 'self':
          $G.searchLocKeywordSkuList(page, selectedLocIds, callback);
          break;
        case 'compete':
          $G.searchLocKeywordCompeteSkuList(selectedLocIds, page, callback);
          break;
        case 'promo':
          $G.searchLocKeywordPromoSkuList(selectedLocIds, page, callback);
          break;
      }
    },

    // 根据查询的关键词过滤命中的SKU结果列表
    searchLocKeywordSkuList: function (p, locIds, callback) {
      var filterKeyword = $.trim($('#J_locFilterKeyword').val());
      var page = p > 0 ? p : 1;

      var iid = layer.load("正在加载数据");
      $.ajax({
        url: Urls.searchLocKeywordSkuList,
        data: {
          "page": page,
          "locIds": locIds,
          "filterKeyword": filterKeyword
        },
        method: 'post',
        dataType: 'json'
      }).always(function () {
        layer.close(iid);
      }).done(function (ret) {
        if (ret['locSkuHtml']) {
          $('#J_locKeywordSkuList').html(ret['locSkuHtml']);
          $('.J_locSkuListBarFixed').pin({
            padding: {
              top: 70
            }
          });
          $G.skuCompare(ret['competeLocList']);
        }
        if (!_.isEmpty(ret['locSkuSimpleList'])) {
          locSkuList = ret['locSkuSimpleList'];
        }

        (ret.result == 'success') && $.when($G.getPrevTopLocKeywordSkuMap(ret['locIds'], ret['skuIds']), $G.searchSkuKeywordEffect(ret['skuIds']));
        ;
        if ($.type(callback) == 'function') {
          callback(ret);
        }
        if (ret.result == 'fail') {
          var tip = (locIds.length == 0) ? '无定位记录，请输入关键词，点击开始定位' : '关键词在指定的页码内未找到本店商品';
          return $('#J_locKeywordSkuList').html('<div class="jumbotron mt_10"><p class="lead text-center">' + tip + '<p></div>');
        }
      });
    },
    searchLocKeywordCompeteSkuList: function (locIds, p, callback) {
      var $t = $('.J_locSkuListContent')
        , p = p > 0 ? p : 1;
      var keyword = $.trim($('#J_locFilterKeyword').val());

      var iid = layer.load("正在加载数据");
      $.ajax({
        url: Urls.searchLocKeywordCompeteSkuList,
        data: {
          "locIds": locIds,
          "page": p,
          "filterKeyword": keyword
        },
        method: 'post',
        dataType: 'json'
      }).always(function () {
        layer.close(iid);
      }).done(function (ret) {
        if (ret.result == 'fail') {
          var tip = '暂无竞品数据，如果你还没添加竞品，请先添加竞品吧。';
          return $('#J_locKeywordCompeteSkuList').html('<div class="jumbotron mt_10"><p class="lead text-center">' + tip + '<p></div>');
        }
        if (ret['skuHtml']) {
          $('#J_locKeywordCompeteSkuList').html(ret['skuHtml']);
          $('.J_locCompteSkuListBarFixed').pin({
            padding: {
              top: 70
            }
          });
        }
        if ($.type(callback) == 'function') {
          callback(ret);
        }
        if (ret['locSkuSimpleList']) {
          locCompeteSkuList = ret['locSkuSimpleList'];
        }
      });
    },
    searchLocKeywordPromoSkuList: function (locIds, p, callback) {
      var p = p > 0 ? p : 1;
      var keyword = $.trim($('#J_locFilterKeyword').val());

      var iid = layer.load("正在加载数据");
      $.ajax({
        url: Urls.searchLocKeywordPromoSkuList,
        data: {
          "locIds": locIds,
          "page": p,
          "filterKeyword": keyword
        },
        method: 'post',
        dataType: 'json'
      }).always(function () {
        layer.close(iid);
      }).done(function (ret) {
        if (ret.result == 'fail') {
          var tip = '该关键词下暂无推广商品，请换一组关键词重新定位。';
          return $('#J_locKeywordPromoSkuList').html('<div class="jumbotron mt_10"><p class="lead text-center">' + tip + '<p></div>');
        }
        if (ret['skuHtml']) {
          $('#J_locKeywordPromoSkuList').html(ret['skuHtml']);
          //$('.J_locCompteSkuListBarFixed').pin({padding: {top: 70}});
        }
        if ($.type(callback) == 'function') {
          callback(ret);
        }
      });
    },
    getPrevTopLocKeywordSkuMap: function (locIds, skuIds) {
      if (_.isEmpty(locIds) || _.isEmpty(skuIds)) {
        return;
      }
      $.ajax({
        url: Urls.getPrevTopLocKeywordSkuMap,
        data: {
          "locIds": locIds,
          "skuIds": skuIds
        },
        method: 'post',
        dataType: 'json'
      }).done(function (ret) {
        if (ret['result'] == 'fail') {
          return;
        }
        var downIcon = '<i class="fa fa-long-arrow-down text-success fa-fw"></i>'
          , upIcon = '<i class="fa fa-long-arrow-up text-danger fa-fw"></i>';
        var pcMap = ret['pcLocMap'] || []
          , appMap = ret['appLocMap'] || []
          , wxMap = ret['mLocMap'] || [];
        $('.J_prevCompare').hide(),
          $.each($('.J_prevCompare'), function () {
            var $t = $(this)
              , locId = $t.data('locId')
              , skuId = $t.data('skuId')
              , platform = $t.data('platform')
              , locInAll = $t.data('locInAll');
            if (platform == 'pc') {
              var cpSkus = _.filter(pcMap, function (itm) {
                return itm['skuId'] == skuId && itm['pLocId'] == locId;
              });
              var k = cpSkus[0];
              if (_.isEmpty(k)) {
                $t.html('<span>' + upIcon + locInAll + '</span>').show();
              } else {
                var diff = locInAll - k['locInAll'];
                (diff == 0) && $t.html('<span class="fc-blue m-l-sm">持平</span>').show();
                (diff > 0) && $t.html('<span>' + downIcon + Math.abs(diff) + '</span>').show();
                (diff < 0) && $t.html('<span>' + upIcon + Math.abs(diff) + '</span>').show();
                $t.tooltip({
                  title: '昨日最高排名：' + k['posFormat']
                });
              }
            } else if (platform == 'app') {
              var cpAppSkus = _.filter(appMap, function (itm) {
                return itm['skuId'] == skuId && itm['pLocId'] == locId;
              });
              var k = cpAppSkus[0];
              if (_.isEmpty(k)) {
                $t.html('<span>' + upIcon + locInAll + '</span>').show();
              } else {
                var diff = locInAll - k['locInAll'];
                (diff == 0) && $t.html('<span class="fc-blue m-l-sm">持平</span>').show();
                (diff > 0) && $t.html('<span>' + downIcon + Math.abs(diff) + '</span>').show();
                (diff < 0) && $t.html('<span>' + upIcon + Math.abs(diff) + '</span>').show();
                $t.tooltip({
                  title: '昨日最高排名：' + k['posFormat']
                });
              }
            } else if (platform == 'm') {
              var cpWxSkus = _.filter(wxMap, function (itm) {
                return itm['skuId'] == skuId && itm['pLocId'] == locId;
              });
              var k = cpWxSkus[0];
              if (_.isEmpty(k)) {
                $t.html('<span>' + upIcon + locInAll + '</span>').show();
              } else {
                var diff = locInAll - k['locInAll'];
                (diff == 0) && $t.html('<span class="fc-blue m-l-sm">持平</span>').show();
                (diff > 0) && $t.html('<span>' + downIcon + Math.abs(diff) + '</span>').show();
                (diff < 0) && $t.html('<span>' + upIcon + Math.abs(diff) + '</span>').show();
                $t.tooltip({
                  title: '昨日最高排名：' + k['posFormat']
                });
              }
            }
          });
      });
    },
    searchSkuKeywordEffect: function (skuIds) {
      var keywords = _.pluck(taskMap, 'keyword');
      $.ajax({
        url: Urls.searchSkuKeywordEffect,
        data: {
          "keywords": keywords,
          "skuIds": skuIds
        },
        method: 'post',
        dataType: 'json'
      }).done(function (ret) {
        if (ret['result'] == 'success') {
          var effectList = ret['keywordListEffect'];
          $.each(effectList, function (skuId, effects) {
            var $item = $('#J_locKeywordSkuList').find('.J_locSkuItem' + skuId);
            if ($item.length == 0) {
              return;
            }
            var format = function (v) {
              return '<span class="p-a-sm">' + v + '</span>';
            }
            $.each(effects, function (hash, effect) {
              $item.find('.J_impression_' + hash).html(format(effect['impression']));
              $item.find('.J_click_' + hash).html(format(effect['click']));
              $item.find('.J_payTradeAmt_' + hash).html(format(effect['pay_trade_amt']));
            });
          });
        }
      });
    },
    skuCompare: function (skuList) {
      if (_.isEmpty(skuList)) {
        return;
      }
      $('#J_locKeywordSkuList .J_compare').popover({
        title: "本店关键词排名与竞品排名比较",
        trigger: "hover",
        content: function () {
          var $t = $(this)
            , locInAll = $t.data('locInAll')
            , platform = $t.data('platform')
            , locId = $t.data('locId');
          var tip = $G.formatPluckCompareSku(skuList, locId, locInAll, platform);
          return tip;
        },
        placement: "right",
        container: "body",
        animation: false,
        html: true,
        template: '' +
        '<div class="popover span4" role="tooltip" style="max-width:300px;">'
        + '<div class="arrow"></div>'
        + '<h3 class="popover-title ft_12"></h3>'
        + '<div class="popover-content ft_12"></div>'
        + '</div>'
      });
    },
    competeCompare: function () {
    },
    formatPluckCompareSku: function (skuList, locId, locInAll, type) {
      var greater = []
        , less = [];
      $.each(skuList, function (i, sku) {
        if ((sku.type != type) || (sku.locId != locId)) {
          return;
        }
        var diffPos = (sku['locInAll'] - locInAll);
        sku['difPos'] = diffPos;
        (diffPos > 0) && less.push(sku);
        (diffPos < 0) && greater.push(sku);
      });
      if (greater.length == 0 && less.length == 0) {
        return '<div class="lead m-b-sm ft_16">该关键词未定位到竞品排名</div>';
      }

      var tip = ''
        , formatSku = function (itemList) {
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

    // TAB下拉框中的历史数据请求处理
    recommendKeywords: function (target, p, callback) {
      var type = 'traffic';
      var page = p > 0 ? p : 1;
      target = target || 'J_locKeywordHistory';
      ZcLog.log(target);
      switch (target) {
        // 定位历史
        case 'J_locKeywordHistory':
          type = 'history';
          break;
        // 到店词推荐
        case 'J_trafficKeywords':
          type = 'traffic';
          break;
        // 我的收藏
        case 'J_fatoriveKeyword':
          type = 'fatorive';
          break;
      }
      var $target = $('#' + target);
      $target.maskLoad({
        'min-height': '200px'
      });
      $.ajax({
        url: Urls.recommendKeywords,
        data: {
          "type": type,
          "page": p
        },
        method: 'get',
        dataType: 'json'
      }).always(function () {
        $target.maskLoad('hide')
      }).done(function (ret) {
        if (ret.result == 'success') {
          $target.empty().html(ret.keywordHtml);
        }
        if ($.type(callback) == 'function') {
          callback(ret);
        }
      });
    },

    // 获取关键词历史组ID
    getLocHistory: function (p) {
      $('.J_locHistoryGroup').maskLoad();
      p = p > 0 ? p : 1;
      $.ajax({
        url: Urls.getLocKeywordHistoryGroup,
        data: {
          "page": p,
          "style": 'locV2'
        },
        method: 'get',
        dataType: 'json'
      }).always(function () {
        $('.J_locHistoryGroup').maskLoad('hide');
      }).done(function (ret) {
        $('.J_locHistoryGroup').html(ret.locHtml);
      });
    },
    showLocChart: function () {
    },
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
    getRandomLocHost: function (uri) {
      var locHost = locHostMap[Math.floor(Math.random() * locHostMap.length)];
      if (!_.isEmpty(uri)) {
        locHost += uri;
      }
      return locHost;
    },
    addLocKeywordMonitor: function () {
      var $t = $(this);
      if ($t.data('added')) {
        return false;
      }
      var keyword = $t.data('keyword')
        , wareId = $t.data('wareId')
        , hash = $t.data('hash');
      if (isEmpty(keyword) || isEmpty(wareId)) {
        layer.alert("参数错误");
      }

      var id = layer.confirm("是否要添加关键词【" + keyword + "】到监控中心？", function () {
        var layerId = layer.load("正在添加关键词");
        $.ajax({
          url: Urls.addLocKeywordMonitor,
          data: {
            "keyword": keyword,
            "wareId": wareId
          },
          method: 'post',
          dataType: 'json'
        }).always(function () {
          layer.close(layerId);
        }).done(function (ret) {
          if (ret.result == 'success') {
            layer.alert("添加监控成功", 9);
            var $select = $('.J_locWareItem' + wareId).find('[data-hash="' + hash + '"]');
            ZcLog.log($select.length);
            $select.addClass('label-success').removeClass('label-primary J_addLocKeywordMonitor');
            $select.data('added', true).html('<i class="fa fa-check-circle mr_5"></i>已监控');
          } else {
            layer.alert(ret.reason);
          }
        });
      });
    },
    printKeywordChart: function (skuId, locId) {
      $('.J_locKeywordModalBody').maskLoad();
      $.ajax({
        url: Urls.locKeywordAndCateSkuChart,
        data: {
          "skuId": skuId,
          "locId": locId,
          "locType": "search"
        },
        method: 'get',
        dataType: 'json'
      }).always(function () {
        $('.J_locKeywordModalBody').maskLoad('hide');
      }).done(function (ret) {
        if ((ret.result == 'success')) {
          $G.format.formatKeywordChart(ret.data, "商品SKU【" + skuId + "】", '#J_keywordLocCharts');
          if (ret.compareData) {
            $('.J_selectIndex').show();
            var idx = $('.J_cpIdxSelect.active').find('a').data('idx');
            var name = $('.J_cpIdxSelect.active').data('title');
            $G.format.compareChartData.data = ret.compareData;
            $G.format.compareChartData.skuId = skuId;
            $G.format.formatKeywordCompareChart('#J_keywordLocCompareCharts', (idx ? idx : 'impression'), (name ? name : '展示次数'));
          }
          if (ret.dataM) {
            $G.format.formatKeywordChart(ret.dataM, "商品SKU【" + skuId + "】", '#J_keywordLocChartsM', {
              'color': '#ec971f',
              'skuPerPage': 10,
              'pageSize': 1000,
              'type': 'M'
            });
          }
          if (ret.dataApp) {
            $G.format.formatKeywordChart(ret.dataApp, "商品SKU【" + skuId + "】", '#J_keywordLocChartsApp', {
              'color': '#ec971f',
              'skuPerPage': 10,
              'pageSize': 1000,
              'type': 'APP'
            });
          }
        } else {
          $('#J_keywordLocCompareCharts, #J_keywordLocChartsM, #J_keywordLocChartsApp').empty().html('<div class="jumbotron lead text-center text-muted mt_10">该SKU无排名信息</div>');
          $('.J_selectIndex').hide();
        }
      });
    },
    printKeywordCompeteSkuChart: function (skuId, locId, competeSkuId) {
      $('.J_locKeywordModalBody').maskLoad();
      $.ajax({
        url: Urls.locKeywordOrCateCompeteSkuChart,
        data: {
          "competeSkuId": competeSkuId,
          "locId": locId,
          "locType": "search"
        },
        method: 'get',
        dataType: 'json'
      }).always(function () {
        $('.J_locKeywordModalBody').maskLoad('hide');
      }).done(function (ret) {
        if ((ret.result == 'success') && ret.data) {
          var titleHtml = ret['data'][0]['wareName'];
          $('#J_locKeywordModal .modal-title').html(titleHtml);
          $G.format.formatKeywordChart(ret.data, "竞品SKU【" + skuId + "】", '#J_keywordLocCharts', {
            "color": '#428bca'
          })
        }
      });
    },
    addPromoSkuToCompete: function (skuId) {
      if (!_.isNumber(skuId)) {
        layer.alert("参数错误");
        return false;
      }
      layer.confirm("确定要添加该商品到竞品中心吗？", function () {
        var layerId = layer.load('正在添加竞品');
        $.ajax({
          url: Urls.addPromoSkuToCompete,
          data: {
            "keyword": skuId
          },
          method: 'post',
          dataType: 'json'
        }).always(function () {
          layer.close(layerId);
        }).done(function (ret) {
          if (ret.result == 'success') {
            layer.msg('添加竞品成功', 2, {
              type: 9
            });
          } else {
            var reason = isEmpty(ret['reason']) ? '添加竞品失败' : ret['reason'];
            layer.alert(reason);
          }
        });
      });
    },
    deleteLocKeywordGroup: function (groupId, callback) {
      var layerId = layer.load('正在删除历史');
      $.ajax({
        url: Urls.delLocKeywordHistoryGroup,
        data: {
          "groupId": groupId
        },
        method: 'post',
        dataType: 'json'
      }).always(function () {
        layer.close(layerId);
      }).done(function (ret) {
        if ($.type(callback) == 'function') {
          callback(ret);
        }
      });
    },
    format: {
      compareChartData: {
        data: {},
        skuId: ''
      },
      formatKeywordChart: function (chartData, chartTitle, displayId, config) {
        if (!chartData) {
          return false;
        }
        var defConf = {
          'type': 'PC',
          'color': '#00aeef'
        }
          , config = ($.type(config) == 'object') ? config : {};
        config = $.extend(defConf, config);

        var titleColor = config.color;
        var h, p, maxPos = 0, fistLoc, psortName, fistp;

        $.each(chartData, function (k, loc) {
          if (k == 0) {
            fistLoc = loc;
          }
          if (loc.rankingNum > 0) {
            maxPos = (maxPos == 0) ? loc.rankingNum : maxPos;
            maxPos = (maxPos > loc.rankingNum) ? loc.rankingNum : maxPos;
          }
          p = loc.rankingNum ? $chart.locPosMap(60, loc.rankingNum) : false;
        });

        /*if($.inArray(config.type, ['M', 'APP']) == -1){
  psortName = $('#J_curLocPsortName').val();
  fistp = (fistLoc.rankingNum > 0 ) ? JX.locChart.locPosMap(60, fistLoc.rankingNum) : false;
  ZcLog.log(fistp);
  fistp = fistp ? '<a class="label danger-bordered">' + fistp.page + '页' + fistp.pos + '位  [' + fistLoc.rankingNum + '名]</a>' : '<span class="label label-default">指定页码内未找到</span>';

  pos = maxPos > 0 ? JX.locChart.locPosMap(60, maxPos) : false;
  maxPos = pos ? '<span class="text-danger">' + pos.page + '页' + pos.pos + '位  [' + maxPos + '名]</span>' : '<span class="text-muted">没有历史最高排名</span>';
  $('#J_locKeywordModal .modal-title').html('<i class="fa fa-area-chart"></i> ' + chartTitle + ' 在搜索页关键词<b class="text-danger">"' + fistLoc.queryWord + '"</b> 的排名速览 ， 最新一次PC端排名为： ' + fistp + ' <a class="label label-success J_curLocPsortName">'+psortName+'</a>');
}*/

        var tname = _.has(config, "type") ? ((config.type == 'M') ? '微信端' : ((config.type == 'APP') ? '安卓App端' : '')) : '';
        chartTitle += '在' + tname + '搜索页关键词  <span class="text-danger">" ' + fistLoc.queryWord + ' "</span> 的排名走势图';

        var setting = {
          "title": chartTitle,
          "color": titleColor
        };
        setting = $.extend(setting, config);
        if ($.inArray(config.type, ['M', 'APP']) != -1) {
          setting.xAxis = true;
        }

        $chart.printCharts(displayId, chartData, setting);
      },
      formatKeywordCompareChart: function (displayId, index, idxName) {
        if (this.compareChartData.data) {
          var config = {
            "index": index,
            "idxName": idxName,
            "title": this.compareChartData.skuId,
            "color": '#00aeef',
            "locType": 'keyword'
          };
          $chart.printCompareChart(displayId, this.compareChartData.data, config);
        }
      },
      bulidSimpleSkus: function (skus, selectSku, locId) {
        var group = '<ul class="box-item-list" style="border: 1px solid #e5e5e5;">';
        $(skus).each(function (k, sku) {
          var locDetail = sku['locList'][locId];
          var locInAll = _.isEmpty(locDetail) ? 0 : parseInt(locDetail['loc_in_all']);
          var loc = locInAll > 0 ? $chart.locPosMap(60, locInAll) : [];

          var itemTpl = '<li class="box-item J_printLocKeywodChart <%= active %>" data-sku-id="<%= skuId %>" data-loc-id="<%= locId %>" data-title="<%= skuTitle %>" style="cursor:pointer;" title="点击查看排名走势">';
          itemTpl += '<div class="media">';
          itemTpl += '  <div class="media-left"><a href="<%= skuUrl %>" target="_blank" title="<%= skuTitle %>"><img src="<%= logoUrl %>" style="width:60px;" class="header-avatar"></a></div>';
          itemTpl += '  <div class="media-body ft_12">';
          itemTpl += '	<a class="label <%= (locInAll > 0) ? \'danger-bordered\' : \'default-bordered\' %>"><%= locLable %></a>';
          itemTpl += '	<div class="ft_12 mt_5">货号：<%= itemNum %></div>';
          itemTpl += '	<div class="ft_12 mt_5">SKU：<%= skuId %></div>';
          itemTpl += '  </div>';
          itemTpl += '</div></li>';
          group += _.template(itemTpl)({
            'active': sku['sku_id'] == selectSku ? 'active' : '',
            'skuId': sku['sku_id'],
            'locId': locId,
            'skuTitle': sku['title'],
            'skuUrl': sku['sku_url'],
            'logoUrl': sku['logo_url'],
            'locInAll': locInAll,
            'locLable': _.isEmpty(loc) ? '指定页码内未找到' : (loc['page'] + '页 ' + loc['pos'] + '位 [' + locInAll + '名]'),
            'itemNum': sku['item_num'],
            'skuId': sku['sku_id']
          });
        });
        group += '</ul>';
        $('.J_bulidSimpleSkus').empty().html(group);
      },
      bulidSimpleCompeteSkus: function (skus, selectSku, locId) {
        var group = '<ul class="box-item-list" style="border: 1px solid #e5e5e5;">';
        $(skus).each(function (k, sku) {
          group += '<li class="box-item J_printLocCompeteChart ' + (sku.sku_id == selectSku ? 'active' : '') + '" data-loc-id="' + locId + '" data-sku-id="' + sku['sku_id'] + '" data-compete-sku-id="' + sku['data_compete_sku_id'] + '" data-pos="modal" style="cursor:pointer;" title="点击查看排名走势">';
          group += '<div class="media">';
          group += '  <div class="media-left"><a href="' + sku.sku_url + '" target="_blank" title="' + sku.title + '"><img src="' + sku.sku_img_url + '" style="width:50px;border:1px solid #a94442;border-radius: 6px;"></a></div>';
          group += '  <div class="media-body ft_12">';
          var locDetail = sku['locList'][locId];
          var locInAll = parseInt(locDetail['loc_in_all']);
          if (locInAll > 0) {
            var loc = $chart.locPosMap(60, locInAll);
            group += '<a class="label danger-bordered">' + loc['page'] + '页 ' + loc['pos'] + '位 [' + locInAll + '名]' + '</a>';
          } else {
            group += '<a class="label label-default">指定页码内未找到</a>';
          }
          group += '<h4 class="ft_12">SkuID：' + (sku.sku_id ? sku.sku_id : '--') + '</h4>';
          group += '</div></li>';
        });
        group += '</ul>';
        $('.J_bulidSimpleSkus').html(group);
      }
    }
  }
  JX.locV3 = new v3();
}(jQuery);


$(function () {
  JX.locV3.init();
  $('[data-toggle="tooltip"], .J_tooltip').tooltip();
  $('.J_bulidSimpleSkus').slimScroll({
    height: '520px',
    railVisible: true
  });
});
