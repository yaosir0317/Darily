var JX = window.JX || {};
(function (JX, $) {
  var loca = window.location;
  var base = loca.protocol + '//' + loca.host, comp = function () {
  };
  var url = {
    // 添加竞品
    addCompeteSku: base + '/data/compete/add_compete_sku',
    // 获取竞品历史信息
    competeSkuLog: base + '/data/compete/compete_sku_log',
    // 删除竞品sku
    deleteCompeteSku: base + '/data/compete/delete_compete_sku',
    // 搜索竞品列表
    searchCompeteList: base + '/data/compete/search_compete_list',
    // 价格图表
    priceChart: base + '/data/compete/priceChart',
    // 评论图表
    commentChart: base + '/data/compete/commentChart',
    // 标题改变历史查询
    titleChangeLog: base + '/data/compete/titleChangeLog',
    // 广告改变历史
    adChangeLog: base + '/data/compete/adChangeLog',
    // 促销改变历史
    promotionsChangeLog: base + '/data/compete/promotionsChangeLog',
    // 添加类目监控
    addToCateMonitor: base + '/data/compete/addToCateMonitor',
    // 取消类目监控
    cancelCateMonitor: base + '/data/compete/cancelCateMonitor',
    // 添加关键词监控
    addToKeywordMonitor: base + '/data/compete/addToKeywordMonitor',
    // 取消关键词监控
    cancelKeywordMonitor: base + '/data/compete/cancelKeywordMonitor',
    // 清除所有动态信息
    clearAllDynamic: base + '/data/compete/clearAllDynamic'
  };

  comp.prototype = {
    init: function () {
      var $t = this;
      $('#J_addCompeteSkuBtn').on('click', $t.addCompeteSku);

      $('.J_skuMapListContent').on('click', '.J_locCompeteModalShow', function () {
        $t.competeSkuLoc($(this));
      });

      $('#J_locCompeteSkuKeyword').on('click', $t.locCompeteSkuKeyword);
      $('.J_skuMapListContent').on('click', '.J_skuListMap .J_deleteCompeteSkuBtn', $t.deleteCompeteSku);

      $('.J_locSearchFilterBtn').on('click', function () {
        var keyword = $.trim($('.J_locSearchFilter').val());
        $('a.J_skuListMapTab[data-type="all"]').tab('show');
        $t.searchCompeteList(1, keyword, 'all', true);
      });
      $('.J_locSearchResetBtn').on('click', function () {
        var locId = $("#J_curLocId").val();
        var ft = $.trim($('.J_locSearchFilter').val());
        if (ft == '') {
          return false;
        }
        $('.J_locSearchFilter').val('');
        $('.J_locSearchFilterBtn').click();
      });

      $('a.J_competeTabs').on('shown.bs.tab', function () {
        var tgt = $(this).data('controls');
        competeId = $('#J_locCompeteSkuId').val();
        $t.competeTabTargetData(tgt, competeId);
      });

      $('a.J_skuListMapTab').on('click', function () {
        if ($(this).parent('li').hasClass('active')) {
          return false;
        }
        var type = $(this).data('type');
        $t.searchCompeteList(1, '', type, false);
      });

      $('.J_skuMapListContent').on('click', '#J_compatePagin li a', function (e) {
        e.preventDefault();
        var $tab = $('li.active a.J_skuListMapTab');
        var type = $tab.data('type');
        var id = $tab.prop('href');
        var p = $(this).data('page-no');

        id = id && id.replace(/.*(?=#[^\s]*$)/, "");
        $t.searchCompeteList(p, '', type, true);
      });

      $('.J_filterDiff').on('click', function () {
        $('.J_filterDiff').removeClass('active btn-info').addClass('btn-default');
        $(this).addClass('active btn-info').removeClass('btn-default');
        $t.searchCompeteList(1, '', 'all', false);
      });

      $('.J_skuMapListContent').on('click', '.J_addCateMonitor', $t.addToCateMonitor);
      $('.J_skuMapListContent').on('click', '.J_cancelCateMonitor', $t.cancelCateMonitor);

      $('.J_skuMapListContent').on('click', '.J_addKeywordMonitor', $t.addToKeywordMonitor);
      $('.J_skuMapListContent').on('click', '.J_cancelKeywordMonitor', $t.cancelKeywordMonitor);

      $('.J_clearAlldynamicBtn').on('click', $t.clearAlldynamic);

      $('.J_skuMapListContent').on('mouseenter', '.J_cancelCateMonitor, .J_cancelKeywordMonitor', function () {
        $(this).addClass('btn-danger').removeClass('btn-default').html('<span class="glyphicon glyphicon-remove"></span> 取消竞品监控');
      }).on('mouseleave', '.J_cancelCateMonitor, .J_cancelKeywordMonitor', function () {
        $(this).addClass('btn-default').removeClass('btn-danger').html('<span class="glyphicon glyphicon-ok"></span> ' + $(this).data('title'));
      });

      $('.J_competeSkus').on('click', '.J_simpleCompeteShow', function () {
        var tgt = $('#J_locCompeteModal .nav-tabs li.active').find('a[data-toggle="tab"]').data('controls');
        var competeId = $(this).data('competeSkuId');
        if (!tgt || competeId <= 0) {
          return false;
        }
        $('#J_locCompeteSkuId').val(competeId);
        $('#J_locCompeteModal').find('.modal-title').html($(this).data('title'));

        $('.J_competeSkus').find('.J_simpleCompeteShow').removeClass('list-group-item-warning');
        $(this).addClass('list-group-item-warning');

        $t.competeTabTargetData(tgt, competeId);
      });

      $('#J_locCompeteModal').on('click', '.J_displayMoreLog', $t.displayMoreLog);
    },
    addCompeteSku: function () {
      var k = $('#J_queryKeyword').val();
      if (!$.trim(k)) {
        layer.alert("请输入SKU ID或者商品链接");
        return false;
      }
      var layerId = layer.load('正在获取竞品信息....');
      $.ajax({
        url: url.addCompeteSku,
        data: {"keyword": k},
        method: 'post',
        dataType: 'json'
      }).always(function () {
        layer.close(layerId);
      }).done(function (ret) {
        if (ret.result == 'success') {
          layer.msg('添加竞品成功', 2, {type: 9});
          location.reload();
        } else {
          var reason = isEmpty(ret['reason']) ? '添加竞品失败' : ret['reason'];
          layer.msg(reason);
        }
      });
    },
    getCompeteSkuLoc: function (competeId) {
      if (competeId <= 0) {
        layer.alert("无效的参数");
        return false;
      }

      $('#J_competeLocLog').maskLoad({"min-height": "150px"});
      $.ajax({
        url: url.competeSkuLog,
        data: {"competeId": competeId},
        method: 'get',
        dataType: 'json'
      }).always(function () {
        $('#J_competeLocLog').maskLoad('hide');
      }).done(function (ret) {
        if (ret.result == 'fail') {
          var html = '<p class="text-center pd_20 text-muted">没有找到任何记录</p>';
          $('#J_competeLocLog').html(html);
        } else {
          var loc, html = '', locInfo;
          locInfo = ret.locInfo;
          loc = parseInt(locInfo.loc_in_all) > 0 ? JX.locChart.locPosMap(60, parseInt(locInfo.loc_in_all)) : false;

          html += '<p>定位时间：' + locInfo.gmt_end_loc + '</p>';
          html += '<p>关键字：<span class="label label-primary">' + locInfo.keyword + '</span><span class="text-muted ft_12"> 已定位 <b class="text-danger">' + locInfo.total_loc + '</b> 次</span></p>';
          if (loc) {
            html += '<p>排　名：<span class="label label-danger">' + '第 ' + loc.page + ' 页 ' + loc.pos + ' 位置附近 </span></p>';
          } else {
            html += '<p>排　名：<span class="text-danger">指定页码内未找到</span></p>';
          }
          $('#J_competeLocLog').html(html);
        }
      });
    },
    competeSkuLoc: function ($t) {
      var sku = $t.closest('.J_competeSkuInfo').data('sku'), competeId = sku['competeId'];
      var tgt = $t.data('target'), $c = this;

      $('a[href="#' + tgt + '"]').tab('show');
      $('#J_locCompeteModal .modal-title').html(sku.title);
      $('#J_locCompeteModal').modal();
      $('#J_locCompeteSkuId').val(competeId);

      if (simpleCompeteSkus.length > 0) {
        $c.bulidSimpleCompeteSkus(simpleCompeteSkus, sku.skuId);
      }

      $c.competeTabTargetData(tgt, competeId);
    },
    deleteCompeteSku: function () {
      var $this = $(this), competeSkuId = $this.data('competeSkuId');
      if (competeSkuId <= 0) {
        layer.alert("数据错误");
        return false;
      }

      var layerId = layer.confirm("删除操作不可逆，确定要删除该竞品吗？", function () {
        layer.close(layerId);
        layerId = layer.load("正在删除竞品");
        $this.addClass('disabled');
        $.ajax({
          url: url.deleteCompeteSku,
          data: {"competeSkuId": competeSkuId},
          method: 'post',
          dataType: 'json'
        }).always(function () {
          $this.removeClass('disabled');
        }).done(function (ret) {
          if (ret.result == 'success') {
            layer.alert('删除成功', 9);
            setTimeout(function () {
              window.location.reload();
            }, 1000);
          } else {
            layer.alert('删除失败【' + ret.reason + '】');
          }
        });
      });
    },
    searchCompeteList: function (p, keyword, type, callback) {
      var $t = $('.J_skuListMap'), p = (p > 0) ? p : 1;
      var diff = $('.J_filterDiff.active').data('diff');
      $t.maskLoad();
      $.ajax({
        url: url.searchCompeteList,
        data: {"page": p, "searchKeyword": keyword, "type": type, "diff": diff},
        method: 'get',
        dataType: 'json'
      }).always(function () {
        $t.maskLoad('hide');
      }).done(function (ret) {
        $t.html(ret.competeHtml);
        if ($.type('callback') == 'function') {
          callback(ret);
        }
      });
    },
    printPriceChart: function (competeId) {
      var id = '#J_competePriceChart';
      if ($(id).data('competeId') == competeId) {
        return false;
      }
      var competeId = competeId > 0 ? competeId : $(this).data('competeId');

      $(id).maskLoad();
      $.ajax({
        url: url.priceChart,
        data: {"competeId": competeId},
        method: 'get',
        dataType: 'json'
      }).always(function () {
        $(id).maskLoad('hide');
      }).done(function (ret) {
        JX.locChart.printCompetePriceChart('.J_competePriceChartShow', ret['pricesData']);
        var html = '<span class="ft_12 mr_10">当前价   <b class="text-danger">￥' + (ret.currPrice > 0 ? ret.currPrice : 0) + '</b> <em class="' + (ret.diff > 0 ? 'text-danger' : 'text-muted') + '">+' + ret.diff + '</em></span>';
        html += '<span class="ft_12"><span class="mr_5">历史最高：<b class="text-danger">￥' + (ret.maxPrice > 0 ? ret.maxPrice : 0) + '</b></span><span class="mr_5">历史均价： <b class="text-muted">￥' + (ret.avgPrice > 0 ? ret.avgPrice : 0) + '</b></span><span class="mr_5">历史最近： <b class="text-success">￥' + (ret.minPrice > 0 ? ret.minPrice : 0) + '</b></span></span>';
        $(id).find('.J_currentCompetePrice').html(html);
        $(id).data('compete-id', competeId);
      });
    },
    printCommentsChart: function (competeId) {
      var id = '#J_competeCommentsChart';
      if ($(id).data('competeId') == competeId) {
        return false;
      }
      var competeId = competeId > 0 ? competeId : $(this).data('competeId');

      $(id).maskLoad();
      $.ajax({
        url: url.commentChart,
        data: {"competeId": competeId},
        method: 'get',
        dataType: 'json'
      }).always(function () {
        $(id).maskLoad('hide');
      }).done(function (ret) {
        ZcLog.log(ret);
        JX.locChart.printCompeteCommentsChart('.J_competeCommentsChartShow', ret['commentsData']);

        var summary = '<ul class="list-unstyled list-inline" style="margin:0;">';
        summary += '<li class="mr_10"><b class="ft_12">评论总数：</b>' + parseInt(ret.totalCnt) + ' <em class="ft_12 ' + (ret.totalGrow ? 'text-danger' : 'text-muted') + '">' + (ret.totalGrow >= 0 ? '+' : '') + parseInt(ret.totalGrow) + '</em></li>';
        summary += '<li class="mr_10"><b class="ft_12">好评数：</b>' + parseInt(ret.goodCnt) + ' <em class="ft_12 ' + (ret.goodCntGrow ? 'text-danger' : 'text-muted') + '">' + (ret.goodCntGrow >= 0 ? '+' : '') + parseInt(ret.goodCntGrow) + '</em></li>';
        summary += '<li class="mr_10"><b class="ft_12">中评数：</b>' + parseInt(ret.generalCnt) + ' <em class="ft_12 ' + (ret.generalCntGrow ? 'text-danger' : 'text-muted') + '">' + (ret.generalCntGrow >= 0 ? '+' : '') + parseInt(ret.generalCntGrow) + '</em></li>';
        summary += '<li class="mr_10"><b class="ft_12">差评数：</b>' + parseInt(ret.poorCnt) + ' <em class="ft_12 ' + (ret.poorCntGrow ? 'text-danger' : 'text-muted') + '">' + (ret.poorCntGrow >= 0 ? '+' : '') + parseInt(ret.poorCntGrow) + '</em></li>';
        summary += '<li class="mr_10"><b class="ft_12">晒单：</b>' + parseInt(ret.showCnt) + ' <em class="ft_12 ' + (ret.showCntGrow ? 'text-danger' : 'text-muted') + '">' + (ret.showCntGrow >= 0 ? '+' : '') + parseInt(ret.showCntGrow) + '</em></li>';
        summary += '</ul>';
        $(id).find('.J_competeCommentsSummary').html(summary);

        $(id).data('compete-id', competeId);
      });
    },
    getCompeteTitleLog: function (competeId, page) {
      var id = '#J_competeTitle';
      var page = page > 0 ? page : 0;
      if (($(id).data('competeId') == competeId) && page == 0) {
        return false;
      }
      if ($(id).data('competeId') != competeId) {
        $(id).find('.J_content').html('');
      }
      var competeId = competeId > 0 ? competeId : $(this).data('competeId');

      $(id).maskLoad();
      $.ajax({
        url: url.titleChangeLog,
        data: {"competeId": competeId, 'page': page},
        method: 'get',
        dataType: 'json'
      }).always(function () {
        $(id).maskLoad('hide');
      }).done(function (ret) {
        $(id).data('compete-id', competeId);
        if (ret.result == 'fail' || !ret.rows) {
          $(id).find('.J_dispalyMore').hide();
          return false;
        }

        var html = '', diff, ds, newest = '';
        var dmp = new diff_match_patch();
        $.each(ret.rows, function (i, v) {
          if (v.original && v.title) {
            diff = dmp.diff_main(v.original, v.title);
            ds = dmp.diff_prettyHtml(diff);
          } else {
            ds = '<span class="text-muted">无差异</span>';
          }

          //newest = (i == 0) ? '<span class="red"> [最新]</span>' : '';
          html += '<tr class="text-left"><td><div class="">标题：' + v.title + newest + '</div>';
          html += '<div class="small text-muted">差异：' + ds + '</div></td>';
          html += '<td><div class="text-center"><span class="text-danger">' + v.date + ' ~ ' + v.endDay + '</div><div class="text-center mt_5">使用<b class="text-danger"> ' + v.diff + ' </b>天</div></td></tr>';
        });
        if (ret.total > 5) {
          $(id).find('.J_dispalyMore').show();
          $(id).find('.J_displayMoreLog').data('page', ret.page);
          $(id).find('.J_displayMoreLog').data('compete-id', competeId);
        }
        if (html) {
          $(id).find('.J_content').append(html);
        }
      });
    },
    getCompeteAdLog: function (competeId, page) {
      var id = '#J_competeAd';
      var page = page > 0 ? page : 0;
      if ($(id).data('competeId') == competeId && page == 0) {
        return false;
      }
      if ($(id).data('competeId') != competeId) {
        $(id).find('.J_content').html('');
      }
      var competeId = competeId > 0 ? competeId : $(this).data('competeId');

      $(id).maskLoad();
      $.ajax({
        url: url.adChangeLog,
        data: {"competeId": competeId, 'page': page},
        method: 'get',
        dataType: 'json'
      }).always(function () {
        $(id).maskLoad('hide');
      }).done(function (ret) {
        $(id).data('compete-id', competeId);
        if (ret.result == 'fail' || !ret.rows) {
          $(id).find('.J_dispalyMore').hide();
          return false;
        }

        var html = '', newest = '';
        if (ret.rows) {
          $.each(ret.rows, function (i, v) {
            //newest = (i == 0) ? '<span class="red"> [最新]</span>' : '';
            html += '<tr class="text-left"><td><div><b class="text-danger">广告词：</b>' + v.ad + newest + '</div>';
            html += '<td><div class="text-center"><span class="text-danger">' + v.date + ' ~ ' + v.endDay + '</div><div class="text-center mt_5">使用<b class="text-danger"> ' + v.diff + ' </b>天</div></td></tr>';
          });
        } else {
          html = '<tr><td colspan="3">没有设定广告词</td></tr>'
        }

        if (ret.total > 5) {
          $(id).find('.J_dispalyMore').show();
          $(id).find('.J_displayMoreLog').data('page', ret.page);
          $(id).find('.J_displayMoreLog').data('compete-id', competeId);
        }
        if (html) {
          $(id).find('.J_content').append(html);
        }
      });
    },
    getCompetePromotionLog: function (competeId) {
      var id = '#J_competePromotions';
      if ($(id).data('competeId') == competeId) {
        return false;
      }
      var competeId = competeId > 0 ? competeId : $(this).data('competeId');

      $(id).maskLoad();
      $.ajax({
        url: url.promotionsChangeLog,
        data: {"competeId": competeId},
        method: 'get',
        dataType: 'json'
      }).always(function () {
        $(id).maskLoad('hide');
      }).done(function (ret) {
        var curHtml = '', preHtml = '', curDate = '', prvDate = '', content = '';
        var nofound = '<div class="text-muted text-center pd_10 ft_12">无促销记录</div>';
        if (!ret) {
          return false;
        }
        $(id).data('compete-id', competeId);
        $.each(ret, function (i, v) {
          if (v.promos.length === 0) {
            return;
          }
          for (var k in v.promos) {
            var promo = v.promos[k];
            content += '<div class="clearfix mb_10">';
            content += '<div class="pull-left"><span style="min-width:36px;padding:1px 2px;color:#fff;background-color:' + ((i == 0) ? '#e4393c' : '#777') + '">' + promo.name + '</span></div>'
            content += '<div style="margin-left:80px;">';

            if (promo.gifts) {
              content += '<div class="ft_12 text-danger">赠送的商品列表' + (promo.content ? ('(' + promo.content + ')') : '') + ((i > 0) ? ('<span class="text-muted"> (从  <span class="text-danger">' + v.date + '</span> 开始)</span>') : '') + '</div>';
              for (var o in promo.gifts) {
                content += '<div class="media" style="margin-top:5px">';
                gift = promo.gifts[o];
                var url = 'http://item.jd.com/' + gift['skuId'] + '.html';
                content += '<div class="media-left"><a href="' + url + '" target="_blank">';
                content += '<img src="' + buildJdImageUrl(gift['imagePath'], 5) + '" style="width:35px"></a></div>';
                content += '<div class="media-body"><a href="' + url + '" target="_blank"><span>' + gift['name'] + '</span></a><span class="text-danger"> x' + gift['number'] + '</span></div>';
                content += '</div>';
              }
            } else {
              content += '<div class="ft_12 text-danger">' + promo.content + (promo.adUrl ? '&nbsp;<a href="' + promo.adUrl + '" target="_blank">详情</a>' : '') + ((i > 0) ? ('<span class="text-muted"> (从  <span class="text-danger">' + v.date + '</span> 开始)</span>') : '') + '</div>';
            }
            content += '</div></div>';
          }

          if (i == 0) {
            curHtml += content;
            curDate = '<span class="ft_12">最新促销  (从 <span class="text-danger">' + v.date + '开始</span> 已持续  <span class="text-danger">' + v.diff + '</span> 天</span>)';
            content = '';
          } else {
            prvDate = '<span class="ft_12">更早促销</span>';
            preHtml += '<div style="border-bottom:1px dashed #009edd;margin-bottom:10px;">' + content + '</div>';
            content = '';
          }
        });
        $(id).find('.J_curPromoStartDate').html(curDate ? curDate : '最新促销');
        $(id).find('.J_currentPromotion').html(curHtml ? curHtml : nofound);

        $(id).find('.J_lastPromoStartDate').html(prvDate ? prvDate : '更早促销');
        $(id).find('.J_lastPromotion').html(preHtml ? preHtml : nofound);
      });
    },
    competeTabTargetData: function (tgt, competeId, page) {
      var $t = this;
      switch (tgt) {
        case 'J_competeQuickLoc':
          $t.getCompeteSkuLoc(competeId);
          break;
        case 'J_competePriceChart':
          $t.printPriceChart(competeId)
          break;
        case 'J_competeCommentsChart':
          $t.printCommentsChart(competeId);
          break;
        case 'J_competePromotions':
          $t.getCompetePromotionLog(competeId);
          break;
        case 'J_competeTitle':
          $t.getCompeteTitleLog(competeId, page);
          break;
        case 'J_competeAd':
          $t.getCompeteAdLog(competeId, page);
          break;
      }
    },
    addToCateMonitor: function (e) {
      e.preventDefault();
      var $t = $(this), compId = $t.data('competeId');
      $t.addClass('disabled');
      $.ajax({
        url: url.addToCateMonitor,
        data: {"competeId": compId},
        method: 'post',
        dataType: 'json'
      }).always(function () {
        $t.removeClass('disabled');
      }).done(function (ret) {
        if (ret.result == 'success') {
          layer.msg('监控成功', 2, {type: 9});
          $t.data('title', '类目已监控');
          $t.addClass('J_cancelCateMonitor btn-default').removeClass('btn-success J_addCateMonitor').html('<span class="glyphicon glyphicon-ok"></span> 类目已监控');
        } else {
          layer.msg(ret.reason, 2);
        }
      });
    },
    cancelCateMonitor: function (e) {
      e.preventDefault();
      var $t = $(this), compId = $t.data('competeId');
      $t.addClass('disabled');
      $.ajax({
        url: url.cancelCateMonitor,
        data: {"competeId": compId},
        method: 'post',
        dataType: 'json'
      }).always(function () {
        $t.removeClass('disabled');
      }).done(function (ret) {
        if (ret.result == 'success') {
          layer.msg('取消成功', 2, {type: 9});
          $t.addClass('J_addCateMonitor btn-default').removeClass('btn-success J_cancelCateMonitor').html('<span class="glyphicon glyphicon-plus"></span> 竞品类目监控');
        } else {
          layer.msg(ret.reason, 2);
        }
      });
    },
    addToKeywordMonitor: function (e) {
      e.preventDefault();
      var $t = $(this), compId = $t.data('competeId');
      $t.addClass('disabled');
      $.ajax({
        url: url.addToKeywordMonitor,
        data: {"competeId": compId},
        method: 'post',
        dataType: 'json'
      }).always(function () {
        $t.removeClass('disabled');
      }).done(function (ret) {
        if (ret.result == 'success') {
          layer.msg('监控成功', 2, {type: 9});
          $t.data('title', '关键词已监控');
          $t.addClass('J_cancelKeywordMonitor btn-default').removeClass('btn-success J_addKeywordMonitor').html('<span class="glyphicon glyphicon-ok"></span> 关键词已监控');
        } else {
          layer.msg(ret.reason, 2);
        }
      });
    },
    cancelKeywordMonitor: function (e) {
      e.preventDefault();
      var $t = $(this), compId = $t.data('competeId');
      $t.addClass('disabled');
      $.ajax({
        url: url.cancelKeywordMonitor,
        data: {"competeId": compId},
        method: 'post',
        dataType: 'json'
      }).always(function () {
        $t.removeClass('disabled');
      }).done(function (ret) {
        if (ret.result == 'success') {
          layer.msg('取消成功', 2, {type: 9});
          $t.addClass('J_addKeywordMonitor btn-default').removeClass('btn-success J_cancelKeywordMonitor').html('<span class="glyphicon glyphicon-plus"></span> 竞品关键词监控');
        } else {
          layer.msg(ret.reason, 2);
        }
      });
    },
    clearAlldynamic: function () {
      var $t = $(this), t = this;
      layer.confirm("确定要清除所有动态吗？", function () {
        var iid = layer.load("正在处理数据...");
        $.ajax({
          url: url.clearAllDynamic,
          method: 'post',
          dataType: 'json'
        }).always(function () {
          layer.close(iid);
        }).done(function (ret) {
          if (ret.result == 'success') {
            $('.J_dynamics').removeClass('red').addClass('text-muted');
            $('.J_dynamics').html('0');
            $t.addClass('hidden');
            JX.compete.searchCompeteList(1, '', 'all', false);
          } else {
            layer.msg(ret.reason, 2);
          }
        });
      });
    },
    bulidSimpleCompeteSkus: function (skus, selectSku) {
      var group = '<ul class="list-group">';
      $(skus).each(function (k, sku) {
        group += '<li class="list-group-item J_simpleCompeteShow ' + (sku.sku_id == selectSku ? 'list-group-item-warning' : '') + '" data-sku-id="' + sku.sku_id + '" data-compete-sku-id="' + sku.compete_id + '" data-title="' + sku.title + '" style="cursor:pointer;" title="点击查看排名走势">';
        group += '<div class="media">';
        group += '  <div class="media-left"><a href="' + sku.sku_url + '" target="_blank" title="' + sku.title + '"><img src="' + sku.sku_img_url + '" style="width:50px;border:1px solid #a94442;border-radius: 6px;"></a></div>';
        group += '  <div class="media-body ft_12">';
        group += '	<div class="text-muted ft_12" style="overflow:hidden;height:36px;line-height:18px;">' + sku.title + '</div>';
        group += '	<div class="ft_12 text-danger">SkuID：' + (sku.sku_id ? sku.sku_id : '--') + '</div>';
        group += '</div></li>';
      });
      group += '</ul>';
      $('.J_competeSkus').html(group);
    },
    displayMoreLog: function () {
      var $this = $(this), target = $this.data('target'), page = $this.data('page');
      var competeId = $this.data('compete-id');
      if (competeId <= 0 || page <= 0) {
        return false;
      }
      JX.compete.competeTabTargetData(target, competeId, page + 1)
    }
  };
  JX.compete = new comp;
}(JX, jQuery));
$(function () {
  JX.compete.init();
  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  });
  $('.J_competeSkus').slimScroll({
    height: '480px',
    railVisible: true
  });
  $('#J_competeTitle .J_slimScroll, #J_competeAd .J_slimScroll, #J_competePromotions .J_slimScroll').slimScroll({
    height: '430px',
    railVisible: true
  });
});
