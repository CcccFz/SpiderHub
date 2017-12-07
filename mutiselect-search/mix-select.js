$(function() {
	var condArr = [];

	$('.mix-select thead').each(function () {
		condArr.push([$(this).attr('class'), []]);
    });

	$('.mix-select tr td').click(function() {
		var $tr = $(this).parent();
		var isChoose = $(this).hasClass('active');
		var idx = $(this).parents('table').index();
		var cond = condArr[idx][1];
		var value = $(this).text();

		if ($(this).index() === 0) {
			$(this).addClass('active');
			$(this).siblings().slice().removeClass('active');
			cond = [] ;
		} else {
			$(this).siblings().eq(0).removeClass('active');

			if (isChoose) {
				$(this).removeClass('active');
				cond = $.grep(cond, function(item) {
 					return item !== value;
				});
			} else {
				$(this).addClass('active');
				cond.push(value);
			}

			if ($tr.children('.active').length === 0) {
				$tr.children('td').eq(0).addClass('active');
			}
		}

		condArr[idx][1] = cond;
		$('#mix-select-result').text(JSON.stringify(condArr, undefined, 4));
	});
});



