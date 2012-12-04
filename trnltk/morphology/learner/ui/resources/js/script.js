/*
 * Copyright  2012  Ali Ok (aliokATapacheDOTorg)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

function initializeLearnerPage() {

    $('.parseResultDetailButton').click(function (e) {
        var self = $(this);
        var parseResultUUID = self.data('parse-result-uuid');
        var detailRow = $('#parse-result-detail-' + parseResultUUID);
        if (!self.attr('fetched-parse-result-detail')) {
            $.get('/parseResultDetail', {'parseResultUUID':parseResultUUID}, function (data) {
                detailRow.find('td').html(data);

                var ua = $.browser;
                if (!ua.mozilla && window['MathJax']) {  // don't trigger MathJax for Firefox since it supports MathMl natively
                    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
                }


                self.attr('fetched-parse-result-detail', true);
                detailRow.toggle();
            })
                .error(function () {
                    alert("Unable to fetch the parse result likelihood calculation detail!");
                });
        }
        else {
            detailRow.toggle();
        }

        e.preventDefault();
    });

    $('.context-word').each(function () {
        var self = $(this);
        var content = '';

        var parseResult = self.data('parse-result');
        if (parseResult) {
            content += '<div class="alert alert-block alert-success" style="text-align: center;">';
            content += '<h3>' + parseResult + '</h3>';
        }
        else {
            content += '<div class="alert alert-block alert-error" style="text-align: center;">';
            content += '<h3>Not parsed yet</h3>';
        }

        content += '<a class="btn btn-large btn-primary" href="learner?wordId=' + self.data('word-id') + '"><i class="icon-arrow-right icon-white"></i> Go</button>';

        content += '</div>';

        self.popover({content:content, trigger:'click', placement:'bottom'});
    });

    $('.context-sentence').each(function () {
        var self = $(this);
        var content = '<button class="btn btn-primary">Go (' + self.data('sentence-id') + ')</button>';
        self.popover({content:content, trigger:'click', placement:'bottom'});
    });
}

function initializeLikelihoodButtons() {

    $('.collocation_detail_button').live('click', function (e) {
        var self = $(this);
        var parseResultId = self.data('parse-result-id');
        var detailRow = $('#collocation-details-' + parseResultId);
        detailRow.toggle();
        e.preventDefault();
    });

    $('.contextless_distribution_detail_button').live('click', function (e) {
        var self = $(this);
        var parseResultId = self.data('parse-result-id');
        var detailRow = $('#contextless-distribution-details-' + parseResultId);
        detailRow.toggle();
        e.preventDefault();
    });

    $('.interpolation_context_detail_button').live('click', function (e) {
        var self = $(this);
        var interpolationContextId = self.data('interpolation-context-id');
        var detailRow = $('#interpolation-context-detail-' + interpolationContextId);
        detailRow.toggle();
        e.preventDefault();
    });

    $('.possibility_context_detail_button').live('click', function (e) {
        var self = $(this);
        self.parents('table:first').find('tr.possibility-context-likelihood-details').toggle();
        e.preventDefault();
    });

}
