var DetailTrigger;

DetailTrigger = (function() {
  function DetailTrigger() {}

  DetailTrigger.prototype.bind = function() {
    var closer, trigger, _i, _j, _len, _len1, _ref, _ref1;
    this.triggers = $('.detail-item.trigger');
    _ref = this.triggers;
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      trigger = _ref[_i];
      $(trigger).click(this.triggerClicked);
    }
    _ref1 = $('.detail-item-closer');
    for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
      closer = _ref1[_j];
      $(closer).click(this.closerClicked);
    }
    return this;
  };

  DetailTrigger.prototype.closerClicked = function(target) {
    $('.detail-item').hide();
    return $('.detail-item.trigger').show('medium');
  };

  DetailTrigger.prototype.triggerClicked = function(target) {
    var trigger, triggered, _i, _len, _ref;
    target = $(target.delegateTarget);
    _ref = $('.detail-item.trigger');
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      trigger = _ref[_i];
      $(trigger).hide();
    }
    $(target).show();
    triggered = $('#' + target.data('triggers'));
    return triggered.removeClass('hidden');
  };

  return DetailTrigger;

})();

if (window.DetailTrigger == null) {
  window.DetailTrigger = DetailTrigger;
}

$(function() {
  return new DetailTrigger().bind();
});
