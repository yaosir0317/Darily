window.JX = window.JX || {};
(function (JX, $) {
  var Host = window.location.protocol + '//' + window.location.host;
  var base = Host + '/data/loc_monitor/', mo = function () {
  };
  var url = {
    // 监控总览
    summary: base + 'summary',
    // 添加关键词到监控
    addKeywordToMonitor: base + 'addKeywordToMonitor',
    // 添加类目到监控
    addCateToMonitor: base + 'addCateToMonitor',
    // 取消关键词监控
    deleteMonitorKeyword: base + 'deleteMonitorKeyword',
    // 取消该商品下的所有关键词监控
    deleteWareAllMonitor: base + 'deleteWareAllMonitor',
    // 取消类目监控
    deleteMonitorCate: base + 'deleteMonitorCate',
    // 获取关键词监控列表
    getKeywordMoniterList: base + 'getKeywordMoniterList',
    // 获取类目监控信息
    getMonitorCateInfo: base + 'getMonitorCateInfo',
    // 搜索监控列表
    searchLocMonitorWareList: base + 'searchLocMonitorWareList',
    // 获取关键词最高排名信息
    getKeywordTopRankSku: base + 'getKeywordTopRankSku',
    // 获取类目最高排名信息
    getCateTopRankSku: base + 'getCateTopRankSku',
    // 获取关键词历史走势
    getKeywordLog: base + 'getKeywordLog',
    // 获取类目历史走势
    getCateLog: base + 'getCateLog',
    // 添加通知邮箱
    addNotifyEmail: base + 'addNotifyEmail',
    // 关键词查询历史信息定位
    recommendKeywords: Host + '/data/loc/recommend_keywords',
    // 一键更新排名
    startRtLocMonitor: base + 'startRtLocMonitor',
    // 循环检测一键更新是否结束
    loopCheckRtLocMonitorEnd: base + 'loopCheckRtLocMonitorEnd',
    // 添加监控商品关注
    addMonitorWareCare: base + 'addMonitorWareCare',
    // 获取商品监控详情
    getWareLocMonitorDetail: base + 'getWareLocMonitorDetail'
  };

  var priv = {
    compareChartData: {data: {}, skuId: ''},
    eachKeywordRow: function (rows) {
      var ks = '';
      if (rows.length <= 0) {
        return '<li class="pd_20 bg-warning text-center ft_18 text-muted"><strong>没有找到任何内容~~~~</strong></li>';
      }
      $.each(rows, function (i, row) {
        ks += '<li class="clearfix pd_10 ft_12">';
        ks += '<div class="col-md-5"><strong>' + row.keyword + '</strong></div>';
        ks += '<div class="col-md-4 text-muted">已监控  <span class="red">' + row.diffDays + '</span> 天</div>';
        ks += '<div class="col-md-3"><button class="btn btn-xs btn-danger J_delMonitorKeyword" data-id="' + row.id + '" data-ware-id="' + row.wareId + '" type="button">删除</button></div>';
        ks += '</li>';
      });
      return ks;
    },
    dispalyCateMonitor: function (resp) {
      var ks = '';
      if (resp.monitorId > 0) {
        ks += '<p class="bg-success pd_20 text-center">类目 【<b>' + resp.breadcrumb + '</b>】 <a class="label label-success"><b class="glyphicon glyphicon-ok"></b> 已监控</a>  ';
        ks += '<a href="javascript:void(0);" data-monitor-id="' + resp.monitorId + '" class="btn btn-xs btn-danger J_delCateMonitor">取消监控</a></p>';
      } else {
        ks += '<p class="bg-warning pd_20 text-center">类目 【<b>' + resp.breadcrumb + '</b>】 <a class="label label-danger"><b class="glyphicon glyphicon-remove"></b> 未监控</a>  ';
        ks += '<a href="javascript:void(0);" data-cid="' + resp.cid + '" data-breadcrumb="' + resp.breadcrumb + '" data-curl="' + resp.cateUrl + '" class="btn btn-xs btn-success J_addCateToMonitor">开启监控</a></p>';
      }
      return ks;
    },
    getMonitorKeywordList: function (wareId) {
      var t = this;
      $('#J_locMonitorKeywordPanel').maskLoad({'min-height': '200px'});
      $.get(url.getKeywordMoniterList, {'wareId': wareId}, function (ret) {
        $('#J_locMonitorKeywordPanel').maskLoad('hide');
        var ks = t.eachKeywordRow(ret.rows);
        if (ks) {
          $('.J_monitorKeywordMap').html(ks);
        }
        if (ret.rows) {
          var kcnt = ret.rows ? ret.rows.length : 0;
          $('.J_keywordMonitorTip_' + wareId).find('.text-danger').html(kcnt);
          $('.J_keywordMonitorTip_' + wareId).removeClass('hidden');
        } else {
          $('.J_keywordMonitorTip_' + wareId).addClass('hidden');
        }
      });
    },
    getMonitorCateInfo: function (wareId) {
      var t = this;
      $('#J_locMonitorCatePanel').maskLoad({'min-height': '200px'});
      $.get(url.getMonitorCateInfo, {'wareId': wareId}, function (ret) {
        $('#J_locMonitorCatePanel').maskLoad('hide');
        if (ret.row) {
          var ks = t.dispalyCateMonitor(ret.row);
        }
        if (ks) {
          $('#J_locMonitorCatePanel').find('.J_cateMonitorInfo').html(ks);
        }
        if (ret.row.monitorId > 0) {
          $('.J_cateMonitorTip_' + wareId).removeClass('hidden');
          $('.J_cateMonitorTip_' + wareId).find('.text-danger').html('【' + ret.row.breadcrumb + '】');
        } else {
          $('.J_cateMonitorTip_' + wareId).addClass('hidden');
        }
      });
    },
    gAjax: function (arg, s, e) {
      var i = {
        url: "/",
        method: "GET",
        queryParams: {},
        dataType: "json",
        context: this,
        timeout: 6e4,
        cache: !1,
        contentType: "application/x-www-form-urlencoded; charset=utf-8"
      }, a = $.extend(true, i, arg);
      $.ajax({
        url: a.url,
        type: a.method,
        data: a.queryParams,
        dataType: a.dataType,
        timeout: i.timeout,
        context: a.context,
        cache: a.cache,
        contentType: a.contentType,
        error: ($.type(e) == 'function') ? e : function () {
        },
        success: ($.type(s) == 'function') ? s : function () {
        }
      });
    },
    bulidMonitorKeywordList: function (keywords, wareId) {
      if (keywords.length <= 0) {
        return false;
      }

      var li = '';
      $(keywords).each(function (k, row) {
        li += '<li><a href="javascript:void(0);" data-monitor-id="' + row.id + '" data-ware-id="' + wareId + '" data-toggle="tooltip" class="panel panel-primary text-primary tag J_monitorkeywordTag" data-original-title="已监控  ' + row.diffDays + ' 天 （点击删除监控词）">' + row.keyword + '</a></li>';
      });
      return li;
    },
    formatKeywordCompareChart: function (displayId, index, idxName) {
      if (this.compareChartData.data) {
        JX.locChart.printCompareChart(displayId, this.compareChartData.data, {
          "index": index,
          "idxName": idxName,
          "title": this.compareChartData.skuId,
          "color": '#00aeef'
        });
      }
    }
  }, $G;
  mo.prototype = {
    init: function () {
      $G = this;
      var $t = this, tb = getValue('tb');
      if (!$('#J_locMonitorWarePan').length) {
        return false;
      }

      $('.J_viewWareList').on('click', 'a[data-toggle="tab"]', function () {
        if ($(this).parent('li').hasClass('active')) {
          return false;
        }
        var tab = $(this).data('tab');
        $('#J_searchLocMonitor input[name="viewTab"]').val(tab);
        (tab == 'monitor') ? $('.J_startRtLocMonitorPan').show() : $('.J_startRtLocMonitorPan').hide();
        $G.searchLocMonitorWareList();
      });

      $('#J_locMonitorWarePan').off('click', '.J_addCateToMonitor').on('click', '.J_addCateToMonitor', function () {
        $G.addCateToMonitor($(this));
      }).on('click', '.J_delCateMonitor', function () {
        $G.delCateMonitor($(this));
      }).on('click', '.J_locSearchFilterBtn', function (e) {
        e.preventDefault();
        $G.searchLocMonitorWareList(1);
      }).on('click', '.J_zcPaginationGroup ul li a', function (e) {
        e.preventDefault();
        $G.searchLocMonitorWareList($(this).data('pageNo'));
      }).on('click', '.J_printLocMonitorChart', function () {
        $G.printLocMonitorChart($(this));
      }).off('click', '.J_bulidKeywordBox').on('click', '.J_bulidKeywordBox', function (e) {
        $G.buildKeywordBox(e, $(this));
      }).on('click', '.J_monitorkeywordTag', function () {
        $G.delMonitorKeyword($(this));
      }).on('click', '.J_cancelMonitor', function () {
        $G.cancelMoniotr($(this))
      }).on('click', '.J_cancelWareAllMonitor', function () {
        $G.cancelWareAllMonitor($(this));
      }).on('click', '.J_addMonitorWareCare', $G.addMonitorWareCare);
      ;

      $G.searchLocMonitorWareList(1, function (mRet) {
        $('[data-toggle="tooltip"]').tooltip({trigger: 'hover'});
      });


      $('.J_addNotifyEmailBtn').on('click', $t.addNotifyEmail);
      $('.J_cpIdxSelect').on('click', function () {
        var idx = $(this).find('a').data('idx'), idxName = $(this).data('title');
        $('.J_cpIdxSelect').removeClass('active');
        $(this).addClass('active');
        $('.J_selectIndex').find('.J_idxName').empty().html(idxName);
        priv.formatKeywordCompareChart('.J_monitorSkuChart', idx, idxName);
      });

      $('#J_locMonitorChartModal').on('click', '.J_printLocMonitorChart', this.printSkuMonitorChart);
      $('#J_locMonitorChartModal').on('click', '.J_printSkuCompeteChart', this.printSkuCompeteMonitorChart);
      $('#J_locMonitorModal a[data-toggle="tab"]').on('click', function () {
        if ($(this).parent('li').hasClass('active')) {
          return false;
        }
        var tId = $(this).data('controls'), wareId = $('.J_monitorWareId').val();
        if (wareId <= 0) {
          return false;
        }
        if (tId == 'J_locMonitorCatePanel') {
          priv.getMonitorCateInfo(wareId);
        }
        if (tId == 'J_locMonitorKeywordPanel') {
          priv.getMonitorKeywordList(wareId);
        }
      });

      var $rtLocBtn = $('#J_startRtLocMonitor');
      $rtLocBtn.on('click', $t.startRtLocMonitor);
      (($rtLocBtn.data('running') == true) && ($rtLocBtn.data('taskId') > 0)) && $t.loopCheckRtLocMonitorEnd($rtLocBtn.data('taskId'));

      $('#J_downloadLocMonitorHistory').on('click', function () {
        $G.dowloadHistoryEvent();
      });
    },
    searchLocMonitorWareList: function (page, callback) {
      var valueMap = $('#J_searchLocMonitor').getFormNV(), $pan = $('#J_locMonitorWarePan');
      valueMap['page'] = page > 0 ? page : 1;
      $pan.maskLoad();
      $.ajax({
        url: url.searchLocMonitorWareList,
        data: valueMap,
        method: 'post',
        dataType: 'json'
      }).always(function () {
        $pan.maskLoad('hide');
      }).then(function (mRet) {
        $pan.find('.J_wareListContent').empty().html(mRet['wareListHtml']);
        _.isFunction(callback) && callback(mRet);
      }, function (event, jqXhr) {
        ZcLog.log(jqXhr);
      });
    },
    printLocMonitorChart: function ($t) {
      var ware = $t.closest('.J_wareInfo').data('ware'), wid = $t.data('wareId');
      var $md = $('#J_locMonitorChartModal'), tp = $t.data('type'),
        mid = (tp == 'keyword') ? $t.data('keywordInfoId') : $t.data('cateInfoId');

      $md.find('.J_monitorSummary').hide();
      $md.find('.modal-title').html(ware.name);
      $md.find('.header-img img').prop('src', ware.img);
      $md.find('.J_monitorWareId').val(ware.wareId);
      $md.find('tr.selected').removeClass('selected');
      $md.find('.J_monitorSkuChart').html('<p class="bg-warning pd_20 text-center mt_20">点击SKU列表中的  【<a class="label danger-bordered"><span class="fa fa-area-chart"></span> 走势</a>】 按钮查看排名走势~~</p>');
      $md.find('.J_selectIndex').hide();
      $md.find('.J_displayMoniotrChart').hide();

      if (tp == 'keyword') {
        if (ware['keyword']) {
          $md.find('.J_monitorSummary > span').html(ware['keyword']);
          $md.find('.J_monitorSummary').show();
        }
      }
      if (tp == 'keyword') {
        var arg = {url: url.getKeywordTopRankSku, queryParams: {wareId: wid, keywordInfoId: mid}};
      } else {
        var arg = {url: url.getCateTopRankSku, queryParams: {wareId: wid, cateInfoId: mid}};
      }

      $('#J_chartSkuId').val('');
      $('#J_monitorSkuInfo').maskLoad();
      priv.gAjax(arg, function (rt) {
        $('#J_monitorSkuInfo').maskLoad('hide');
        if (rt.result == 'fail') {
          return layer.alert(rt.reason);
        } else {
          var r = '', j = 1, c = '';
          $.each(rt.topSkus, function (i, sku) {
            var a = JX.locChart.locPosMap(60, sku.locInAll), e = "", loc = parseInt(sku.locInAll),
              diff = parseInt(sku.rankDiff);
            var us = '', ue = '';
            if (tp == 'cate' && sku.cateUrl != '' && a.page > 0) {
              us = '<a href="' + sku.cateUrl + '&page=' + a.page + '&JL=6_0_0&area=1,72,2799" target="_blank" class="label label-danger">';
              ue = '</a>';
            }
            if (_.has(sku, 'jdSearchUrl')) {
              us = '<a href="' + sku.jdSearchUrl + '" target="_blank" class="label danger-bordered">';
              ue = '</a>';
            } else {
              if (tp == 'keyword' && a.page > 0 && sku.keyword) {
                var tpl = 'http://search.jd.com/Search?keyword=' + sku.keyword + '&enc=utf-8&qrst=1&ps=addr&rt=1&stop=1&click=&psort=&page=' + a.page + '&area=1';
                us = '<a href="' + tpl + '" target="_blank" class="label danger-bordered">';
                ue = '</a>';
              }
            }
            loc <= 0 || isNaN(loc) ? e = '未进前60页' : (e = us + "第" + a.page + "页" + a.pos + "位" + ue);
            r += '<tr>';
            r += '	<td class="text-center" style="width:40px;">' + j + '</td>';
            r += '	<td class="text-left"><div class="text-muted">SKUID : <span class="text-danger">' + sku.sku_id + '</span></div>';
            if (sku.sku_sub_name) {
              r += '<div>属性 : <span class="text-danger">' + sku.sku_sub_name + '</span></div>';
            } else if (sku.color_value || sku.size_value) {
              r += '<div>属性 : <span class="text-danger">' + (sku.color_value ? sku.color_value : '--') + (sku.size_value ? (' // ' + sku.size_value) : '') + '</span></div>';
            }
            r += '  </td>';
            r += '	<td class="text-left text-muted">' + e + '</td>';
            r += '	<td class="text-left text-muted clearfix"><div class="w62 pull-left mt_5">' + ((loc <= 0 || isNaN(loc)) && isNaN(diff) ? '--' : '<span class="text-danger">' + Math.abs(diff) + '</span><span class="glyphicon ' + (sku.change == 'down' ? 'glyphicon-arrow-down text-success' : 'glyphicon-arrow-up text-danger') + '"></span>') + '</div>';
            r += '	<div class="pull-left"><a href="javascript:void(0);" data-type="' + tp + '" class="J_printLocMonitorChart label label-danger" data-sku-id="' + sku.sku_id + '" data-info-id="' + mid + '"><span class="fa fa-area-chart"></span> 走势</a></div></td>';
            r += '</tr>';
            j++;
          });
          r && $('.J_monitorSkuList').html(r);
          if (rt.competeSkus) {
            $.each(rt.competeSkus, function (i, sku) {
              c += '<tr><td class="text-left">';
              c += '<div class="media">';
              c += '  <div class="media-left">';
              c += '    <a><img src="' + sku.sku_img_url + '" style="width:45px;"></a>';
              c += '  </div>';
              c += '  <div class="media-body"><div class="ft_12 text-muted" style="height:28px;line-height:14px;overflow:hidden;">' + sku.title + '</div>';
              c += '    <div class="mt_5"><span class="text-muted mr_10">价格：<b class="text-danger">¥' + ((sku.price > 0) ? sku.price : 0) + '</b></span><a href="javascript:void(0);" data-type="' + tp + '" class="J_printSkuCompeteChart btn btn-primary btn-xs disabled" data-comp-sku-id="' + sku.sku_id + '" data-info-id="' + mid + '"><span class="fa fa-line-chart"></span> 对比</a></div>';
              c += '  </div>';
              c += '</div>';
              c += '</td></tr>';
            });
            c && $('.J_monitorCompeteSkuList').html(c);
          }
        }
      }, function () {
        $('#J_monitorSkuInfo').maskLoad('hide');
        layer.msg("载入数据出错", 2);
      });
      $md.modal();
    },
    printSkuMonitorChart: function () {
      var $t = $(this), tp = $t.data('type'), skuId = $t.data('skuId'), infoId = $t.data('infoId');
      if (!tp || skuId <= 0 || infoId <= 0) {
        layer.alert("参数错误");
        return false;
      }
      $('.J_monitorSkuList tr').removeClass('selected');

      $('#J_locMonitorChartModal').find('.J_displayMoniotrChart').show();
      if (tp == 'cate') {
        $('#J_locMonitorChartModal').find('a[data-toggle="tab"]:first').tab('show');
        $('#J_locMonitorChartModal').find('.J_monitorChartM').hide();
      }

      if (tp == 'keyword') {
        var argus = {keywordInfoId: infoId, skuId: skuId}
        var u = {url: url.getKeywordLog, queryParams: argus};
        $('#J_monitorSkuInfo').maskLoad();
        $t.closest('tr').addClass('selected');
        priv.gAjax(u, function (ret) {
          $('#J_monitorSkuInfo').maskLoad('hide');
          $('.J_chartSkuId').val(skuId);
          if (ret.result == 'success') {
            //JX.locChart.printCharts('.J_monitorSkuChart', ret.rows, {'title' : 'SKU：' + skuId + '的排名走势'});
            $('.J_selectIndex').show();
            var idx = $('.J_cpIdxSelect.active').find('a').data('idx');
            var name = $('.J_cpIdxSelect.active').data('title');

            priv.compareChartData.data = ret.rows;
            priv.compareChartData.skuId = skuId;
            priv.formatKeywordCompareChart('.J_monitorSkuChart', (idx ? idx : 'impression'), (name ? name : '展示次数'));

            if (ret.rowsM) {
              JX.locChart.printCharts('.J_monitorSkuChartM', ret.rowsM, {
                'title': "微信端商品SKU【" + skuId + "】的监控排名走势",
                'color': '#ec971f',
                'skuPerPage': 10,
                'pageSize': 1200
              });
            }
            if (ret.rowsApp) {
              JX.locChart.printCharts('.J_monitorSkuChartApp', ret.rowsApp, {
                'title': "安卓App端商品SKU【" + skuId + "】的监控排名走势",
                'color': '#ec971f',
                'skuPerPage': 10,
                'pageSize': 1200
              });
            }

            $('.J_printSkuCompeteChart').removeClass('disabled');
          }
        }, function () {
          $('#J_monitorSkuInfo').maskLoad('hide');
          layer.alert("数据载入错误");
        });
      }
      if (tp == 'cate') {
        var argus = {cateInfoId: infoId, skuId: skuId}
        var u = {url: url.getCateLog, queryParams: argus};

        $('#J_monitorSkuInfo').maskLoad();
        $t.closest('tr').addClass('selected');
        priv.gAjax(u, function (ret) {
          $('#J_monitorSkuInfo').maskLoad('hide');
          $('.J_chartSkuId').val(skuId);
          if (ret.result == 'success') {
            JX.locChart.printCharts('.J_monitorSkuChart', ret.rows, {
              'locType': 'cate',
              'title': 'SKU：' + skuId + '的类目排名走势'
            });
            $('.J_printSkuCompeteChart').removeClass('disabled');
          }
        }, function () {
          $('#J_monitorSkuInfo').maskLoad('hide');
          layer.alert("数据载入错误");
        });
      }
    },
    printSkuCompeteMonitorChart: function () {
      var $t = $(this), tp = $t.data('type'), cmpId = $t.data('compSkuId'), infoId = $t.data('infoId'),
        sId = parseInt($('.J_chartSkuId').val());
      if (!tp || infoId <= 0 || cmpId <= 0 || (sId <= 0 || isNaN(sId))) {
        layer.alert("参数错误");
        return false;
      }

      $('.J_monitorCompeteSkuList tr').removeClass('selected');
      if (tp == 'keyword') {
        var argus = {keywordInfoId: infoId, competeSkuId: cmpId, skuId: sId};
        var u = {url: url.getKeywordLog, queryParams: argus};

        $('#J_monitorSkuInfo').maskLoad();
        $t.closest('tr').addClass('selected');
        priv.gAjax(u, function (ret) {
          $('#J_monitorSkuInfo').maskLoad('hide');
          if (ret.result == 'success') {
            JX.locChart.printMonitorCompeteChart('.J_monitorSkuChart', ret.rows, {'title': 'SKU：' + sId + '和竞品（SKU：' + cmpId + '）的排名对比'});
          }

        }, function () {
          $('#J_monitorSkuInfo').maskLoad('hide');
          layer.alert("数据载入错误");
        });
      }
      if (tp == 'cate') {
        var argus = {cateInfoId: infoId, competeSkuId: cmpId, skuId: sId};
        var u = {url: url.getCateLog, queryParams: argus};

        $('#J_monitorSkuInfo').maskLoad();
        $t.closest('tr').addClass('selected');
        priv.gAjax(u, function (ret) {
          $('#J_monitorSkuInfo').maskLoad('hide');
          if (ret.result == 'success') {
            JX.locChart.printMonitorCompeteChart('.J_monitorSkuChart', ret.rows, {'title': 'SKU：' + sId + '和竞品（SKU：' + cmpId + '）的类目排名对比'});
          }
        }, function () {
          $('#J_monitorSkuInfo').maskLoad('hide');
          layer.alert("数据载入错误");
        });
      }
    },
    setLocMonitor: function () {
      var ware = $(this).closest('.J_wareInfo').data('ware'), tId = $(this).data('target');
      var $md = $('#J_locMonitorModal');

      $md.find('.modal-title').html(ware.name);
      $md.find('.header-img img').prop('src', ware.img);
      $md.find('.J_monitorWareId').val(ware.wareId);

      if (tId == 'J_locMonitorCatePanel') {
        priv.getMonitorCateInfo(ware.wareId);
      }
      if (tId == 'J_locMonitorKeywordPanel') {
        priv.getMonitorKeywordList(ware.wareId);
      }

      $('a[href="#' + tId + '"]').tab('show');
      $md.modal();
    },
    addKeywordToMonitor: function (wareId, keywords) {
      var $this = $(this);
      if (!_.isNumber(wareId) || _.isEmpty(keywords)) {
        layer.alert("参数错误，关键词为空");
        return false;
      }
      var keyword = keywords.join(',');
      var iid = layer.load("正在保存关键词");
      $.ajax({
        url: url.addKeywordToMonitor,
        data: {"keyword": keyword, "wareId": wareId},
        method: 'post',
        dataType: 'json'
      }).always(function () {
        layer.close(iid);
      }).done(function (ret) {
        if (ret.result == 'fail') {
          layer.alert(ret.reason);
          return false;
        }
        $G.getWareLocMonitorDetail(wareId);
        /*var li = priv.bulidMonitorKeywordList(ret.rows, wareId);
        if(li != false){
          $('.J_monitorKeyword_' + wareId).html(li);
        }
        $('#J_textareaKeyword').val('');
        $('.J_monitorkeywordTag').tooltip();*/
      });
    },
    addCateToMonitor: function ($t) {
      var cid = $t.data('cid'), wareId = $t.data('wareId');
      if (cid <= 0 || wareId <= 0) {
        layer.alert("参数错误");
        return false;
      }

      $t.addClass('disabled');
      var iid = layer.load("正在添加类目监控");
      $.ajax({
        url: url.addCateToMonitor,
        data: {"wareId": wareId, "cid": cid},
        method: 'post',
        dataType: 'json'
      }).always(function () {
        $t.removeClass('disabled');
        layer.close(iid);
      }).done(function (ret) {
        ZcLog.log(ret);
        if (ret.result == 'fail') {
          layer.alert(ret.reason);
          return false;
        }

        $G.getWareLocMonitorDetail(wareId);
      });
    },
    delMonitorKeyword: function ($t) {
      var mid = $t.data('monitorId'), wid = $t.data('wareId');
      if (mid <= 0 || wid <= 0) {
        layer.alert("参数错误");
        return false;
      }

      layer.confirm("确认删除该条关键词监控吗？", function () {
        var iid = layer.load("正在处理数据");
        $.ajax({
          url: url.deleteMonitorKeyword,
          data: {"monitorId": mid, "wareId": wid},
          method: 'post',
          dataType: 'json'
        }).always(function () {
          layer.close(iid);
        }).done(function (ret) {
          if (ret.result == 'fail') {
            layer.alert(ret.reason);
            return false;
          }

          $G.getWareLocMonitorDetail(wid);

          /*var li = priv.bulidMonitorKeywordList(ret.rows, wid);
          $('.J_monitorKeyword_' + wid).html(li ? li : '');
          $('.J_monitorkeywordTag').tooltip();*/
        });
      });
    },
    delCateMonitor: function ($t) {
      var mid = $t.data('monitorId'), wid = $t.data('wareId');
      if (mid <= 0) {
        layer.alert("参数错误");
        return false;
      }

      layer.confirm("确认取消类目监控吗？", function () {
        var iid = layer.load("正在处理数据");
        $.ajax({
          url: url.deleteMonitorCate,
          data: {"monitorId": mid, "wareId": wid},
          method: 'post',
          dataType: 'json'
        }).always(function () {
          layer.close(iid);
        }).done(function (ret) {
          ZcLog.log(ret);
          if (ret.result == 'fail') {
            layer.alert(ret.reason);
            return false;
          }

          $G.getWareLocMonitorDetail(wid);
          /*$t.closest('.J_cateMoitor').find('.has-success, .alert-success, .glyphicon-ok').each(function(){
            $(this).hasClass('has-success') && $(this).removeClass('has-success').addClass('has-warning');
            $(this).hasClass('alert-success') && $(this).removeClass('alert-success').addClass('alert-warning');
            $(this).hasClass('glyphicon-ok') && $(this).removeClass('glyphicon-ok').addClass('glyphicon-warning-sign');
          });

          $t.data('cid', ret['cid']);
          $t.data('breadcrumb', ret['cate_breadcrumb']);
          $t.data('curl', ret['cate_url']);
          $t.removeClass('btn-danger J_delCateMonitor').addClass('btn-success J_addCateToMonitor').html('开启');*/
        });
      });
    },
    cancelMoniotr: function ($t) {
      var mid = $t.data('monitorId'), wid = $t.data('wareId'), type = $t.data('type'),
        id = (type == 'cate') ? '#J_spuListCate' : '#J_spuListKeyword';
      if (mid <= 0) {
        layer.alert("参数错误");
        return false;
      }
      layer.confirm("确定要取消该监控吗？", function () {
        var iid = layer.load("正在处理数据");
        $.ajax({
          url: (type == 'cate') ? url.deleteMonitorCate : url.deleteMonitorKeyword,
          data: {"monitorId": mid, "wareId": wid},
          method: 'post',
          dataType: 'json'
        }).always(function () {
          layer.close(iid);
        }).done(function (ret) {
          if (ret.result == 'fail') {
            layer.alert(ret.reason);
            return false;
          }

          $G.getWareLocMonitorDetail(wid);
        });
      });
    },
    cancelWareAllMonitor: function ($t) {
      var wareId = $t.data('wareId');
      layer.confirm("确定要取消该商品的所有监控吗？", function () {
        var iid = layer.load("正在处理数据");
        $.ajax({
          url: url.deleteWareAllMonitor,
          data: {"wareId": wareId},
          method: 'post',
          dataType: 'json'
        }).always(function () {
          layer.close(iid);
        }).done(function (ret) {
          if (ret.result == 'fail') {
            layer.alert(ret.reason);
            return false;
          }

          $G.searchLocMonitorWareList(1);
        });
      });
    },
    addNotifyEmail: function () {
      var email = $.trim($('.J_notifyEmail').val());
      var u = url.addNotifyEmail;
      priv.gAjax({url: u, method: 'post', queryParams: {'email': email}}, function (ret) {
        return (ret.result == 'success') ? layer.alert('添加/修改成功', 9) : layer.alert('添加/修改失败');
      }, function () {
        layer.alert("数据错误");
      });
    },
    buildKeywordBox: function (e, $this) {
      var wareId = $this.data('wareId'), $panel = $this.next('.J_keywordAddPanel'),
        tplContent = $('#J_addMoniotrKeywordTpl').html();
      var keywordBox = [], Monitor = {
        addKeywordsToBox: function (keyword) {
          var keyword = $.trim(keyword);
          if (_.isEmpty(keyword) || ($.inArray(keyword, keywordBox) !== -1)) {
            return false;
          }
          keywordBox.push(keyword);
          this.buidHtml();
        },
        removeKeywordsFromBox: function (keyword) {
          var idx = $.inArray(keyword, keywordBox);
          if (_.isEmpty(keyword) || (idx === -1)) {
            return false;
          }
          keywordBox.splice(idx, 1);
          this.buidHtml();
        },
        buidHtml: function () {
          var qhtml = '', $c = $('.J_keywordAddPanel').find('.J_monitorKeywordList');
          if (keywordBox.length == 0) {
            $c.html('');
          }
          for (var i in keywordBox) {
            var compiled = _.template('<span class="tag label label-info J_keyword" data-keyword="<%= locKeyword %>"><%= locKeyword %><span data-role="remove" data-keyword="<%= locKeyword %>"></span></span>')({locKeyword: keywordBox[i]});
            qhtml += compiled
          }
          $c.html(qhtml);
        }
      };
      $panel.on('click', function (e) {
        e.stopPropagation();
      });
      $('.J_keywordAddPanel').empty();
      $panel.html(tplContent);

      $this.parent('.dropdown').off('shown.bs.dropdown').on('shown.bs.dropdown', function () {
        $G.recommendKeywords(1, function () {
          $('.J_recommendKeywordPanel').on('click', '.J_zcPaginationGroup ul > li > a', function (e) {
            e.preventDefault();
            $G.recommendKeywords($(this).data('pageNo'));
          });
        });
      });
      $('.J_monitorKeywordList').on('click', '[data-role="remove"]', function () {
        Monitor.removeKeywordsFromBox($(this).data('keyword'));
      });
      $('.J_enterKeyword').on('keypress', function (e) {
        var keyword = $(this).val();
        if (e.keyCode == 13) {
          Monitor.addKeywordsToBox(keyword);
          $(this).val('');
        }
      });
      $('.J_keywordAddPanel').find('a[data-toggle="tab"]').on('click', function (e) {
        e.preventDefault();
        $(this).tab('show');
        $G.recommendKeywords($(this).data('pageNo'));
      });
      $('.J_keywordAddPanel').find('.J_removePanel').on('click', function () {
        $(this).closest('.dropdown.open').removeClass('open');
      });
      $('.J_keywordAddPanel').on('click', '.J_addKeywordToMonitor', function () {
        var keyword = $.trim($(this).data('keyword'));
        if (keyword) {
          Monitor.addKeywordsToBox(keyword);
        }

        if (keywordBox.length == 0) {
          layer.alert("请输入监控关键词");
          return false;
        }
        $G.addKeywordToMonitor(wareId, keywordBox);
      });
    },
    recommendKeywords: function (p, callback) {
      var id = $('.J_spuListContent').find('.J_recommendKeywords > li.active > a').data('tab');
      var type = (id == 'J_trafficKeywords') ? 'traffic' : 'fatorive', $target = $('.J_spuListContent').find('#' + id);
      var page = p > 0 ? p : 1;

      $target.maskLoad();
      $.ajax({
        url: url.recommendKeywords,
        data: {"type": type, "page": p, "src": "locMonitor"},
        method: 'get',
        dataType: 'json'
      }).always(function () {
        $target.maskLoad('hide')
      }).done(function (ret) {
        if (ret.result == 'success') {
          $target.html(ret.keywordHtml);
        }
        if ($.type(callback) == 'function') {
          callback(ret);
        }
      });
    },
    startRtLocMonitor: function () {
      var $t = $(this), self = this;
      $t.addClass('disabled').prop('disabled', true).html('<i class="fa fa-refresh fa fa-fw fa-spin"></i>定位运行中...');
      $.ajax({
        url: url.startRtLocMonitor,
        method: 'post',
        dataType: 'json'
      }).then(function (ret) {
        if (ret.result == 'success') {
          return $G.loopCheckRtLocMonitorEnd(ret['taskId']);
        }
        return layer.alert(ret['reason'] || '实时定位失败'), $t.removeClass('disabled').prop('disabled', false).html('<i class="fa fa-refresh fa fa-fw"></i>一键刷定位排名');
      }, function () {
        layer.alert("系统错误，请联系客服"), $t.removeClass('disabled').prop('disabled', false).html('<i class="fa fa-refresh fa fa-fw"></i>一键更新排名');
      });
    },
    loopCheckRtLocMonitorEnd: function (taskId) {
      var self = this, taskId = taskId || '';
      $.ajax({
        url: url.loopCheckRtLocMonitorEnd,
        method: 'post',
        data: {'taskId': taskId},
        dataType: 'json'
      }).then(function (checkRet) {
        if (checkRet['status'] == 'finish') {
          return layer.msg("定位完成", 2, 9), window.location.reload();
        }
        setTimeout(function () {
          $G.loopCheckRtLocMonitorEnd(taskId);
        }, 3000);
      });
    },
    addMonitorWareCare: function () {
      var $t = $(this), wareId = $t.data('wareId'), action = $t.data('action');
      var doCareMonitorWare = function () {
        var iid = layer.load("正在处理数据");
        $.ajax({
          url: url.addMonitorWareCare,
          data: {"wareId": wareId, "action": action},
          method: 'post',
          dataType: 'json'
        }).always(function () {
          layer.close(iid);
        }).done(function (ret) {
          if (ret.result == 'success') {
            if (action == 'add') {
              var tipTitle = '【取消关注】取消之后商品将不会拍在前面';
              $t.find('.fa').addClass('fa-heart fc-red').removeClass('fa-heart-o'), $t.data('action', 'cancel');
            } else {
              var tipTitle = '【关注该商品】关注之后该商品会排在前面';
              $t.find('.fa').removeClass('fc-red').addClass('fa-heart-o'), $t.data('action', 'add');
            }
            $t.attr('title', tipTitle).tooltip('fixTitle').tooltip('hide');
          } else {
            layer.alert(ret['reason'] || "操作失败");
          }
        });
      }
      if (action == 'add') {
        return doCareMonitorWare();
      }
      layer.confirm("取消关注将会取消该商品下的所有sku的关注信息，确定要取消吗？", function () {
        return doCareMonitorWare();
      })
    },
    getWareLocMonitorDetail: function (wareId) {
      var $pan = $('#J_locMonitorWare' + wareId);
      $pan.maskLoad({'min-height': '150px'});
      $.ajax({
        url: url.getWareLocMonitorDetail,
        data: {"wareId": wareId},
        method: 'post',
        dataType: 'json'
      }).always(function () {
        $pan.maskLoad('hide');
      }).done(function (ret) {
        $pan.find('#J_wareLocMonitorList' + wareId).empty().html(ret['detailHtml']);
      });
    },
    dowloadHistoryEvent: function () {
      var $md = $('#J_downloadLocMonitorLogModal');
      $md.modal();
    }
  };

  JX.locMonitor = new mo;
}(JX, jQuery));

$(function () {
  JX.locMonitor.init();
  $('.J_monitorSkuMaps, .J_monitorCompteSkuMaps').slimScroll({
    height: '210px',
    railVisible: true
  });
});