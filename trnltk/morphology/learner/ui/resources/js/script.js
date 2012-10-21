function initializeLearnerPage() {
    var img = '	\
	<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">	\
			  <mi>x</mi> <mo>=</mo>	\
			  <mrow>	\
				<mfrac>	\
				  <mrow>	\
					<mo>&#x2212;</mo>	\
					<mi>b</mi>	\
					<mo>&#x00B1;</mo>	\
					<msqrt>	\
					  <msup><mi>b</mi><mn>2</mn></msup>	\
					  <mo>&#x2212;</mo>	\
					  <mn>4</mn><mi>a</mi><mi>c</mi> \
					</msqrt> \
				  </mrow> \
				  <mrow> <mn>2</mn><mi>a</mi> </mrow> \
				</mfrac> \
			  </mrow> \
			  <mtext>.</mtext> \
			</math> \
	';

    $('.ajaxFocusPopover').popover({content:img, trigger:'manual', placement:'bottom'}).click(function (e) {
        $(this).popover('toggle');
        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
        e.preventDefault();
    });

    $('.context-word').each(function () {
        var self = $(this);
        var content = '';

        var parseResult = self.data('parse-result');
        if(parseResult){
            content += '<div class="alert alert-block alert-success" style="text-align: center;">';
            content += '<h3>' + parseResult + '</h3>';
        }
        else{
            content += '<div class="alert alert-block alert-error" style="text-align: center;">';
            content += '<h3>Not parsed yet</h3>';
        }

        content += '<a class="btn btn-large btn-primary" href="learner?wordId=' + self.data('word-id') + '"><i class="icon-arrow-right icon-white"></i> Go</button>';

        content += '</div>'

        self.popover({content:content, trigger:'click', placement:'bottom'});
    });

    $('.context-sentence').each(function () {
        var self = $(this);
        var content = '<button class="btn btn-primary">Go (' + self.data('sentence-id') + ')</button>';
        self.popover({content:content, trigger:'click', placement:'bottom'});
    });
}