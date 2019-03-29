function isEmpty(obj) {
  if (_.isNumber(obj) && (obj !== 0)) {
    return false;
  }
  if (_.isObject(obj)) {
    return _.keys(obj).length === 0
  }
  return _.isEmpty(obj);
}

// 搜索下拉框加载loading
!function ($) {
  var SearchLoad = function (element, options) {
    this.$element = $(element);
    this.options = ($.type(options) == 'object') ? $.extend({}, SearchLoad.DEFAULTS, options) : SearchLoad.DEFAULTS;
    if (options == 'hide') {
      return this.remove();
    }
    this.build();
  };
  SearchLoad.DEFAULTS = {
    'min-height': '300px'
  };
  SearchLoad.prototype.build = function () {
    if (this.$element.css("position") != 'relative') {
      this.options.position = 'relative';
    }
    var host = window.location.protocol + '//' + window.location.host;
    var m = '<div class="J_maskLoading_" style="z-index:1020; background-color:#000;opacity:0.3;filter:alpha(opacity=30);top:0;left:0;width:100%;height: 100%; position:absolute;"></div>';
    m += '<div class="J_maskLoading_" style="z-index:1021;left:48%;top:45%;position:absolute;">';
    m += ' <div style="z-index:1022;padding:5px;position: absolute;">';
    m += '	<i class="fa fa-spinner fa-spin" style="font-size:36px;color:#fff;"></i>'
    m += ' </div>';
    m += '</div>';
    this.$element.css(this.options);
    this.$element.find('.J_maskLoading_').remove();
    this.$element.append(m);
  };
  SearchLoad.prototype.remove = function () {
    this.$element.find('.J_maskLoading_').remove();
  }

  function Plugin(options) {
    return this.each(function () {
      return new SearchLoad(this, options);
    })
  }

  $.fn.searchLoad = Plugin;
}(jQuery);

// 全局CSRF_TOKEN
$(function () {
  $(document).ajaxSend(function (e, xhr, options) {
    var header = $("meta[name='csrf_param']").attr("content");
    var token = $("meta[name='csrf_token']").attr("content");
    xhr.setRequestHeader(header, token);
  });
  var wt = $(window).height() - 130;
  var jt = $('#J_maxContainer').height();
  wt > jt ? $('#J_maxContainer').css({"min-height": wt + "px"}) : "";
});
