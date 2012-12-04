"""
Copyright  2012  Ali Ok (aliokATapacheDOTorg)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from bson.code import Code

class NgramTypeFrequencyFinder(object):
    @classmethod
    def find_frequency_of_frequency(cls, collection, ngram_type, frequency):
        """
        Finds the frequency of given frequency.

        For frequency 0, this method should not be used!

        @type collection: Collection
        @type ngram_type: list
        @type frequency: int
        @rtype: int
        """
        assert frequency and frequency > 0

        emission_keys = cls._create_emission_keys(ngram_type)

        filter_criteria = {"value.count": frequency}
        return cls._find_count(collection, emission_keys, filter_criteria)

    @classmethod
    def find_frequency_of_parse_result_frequency(cls, unigram_collection, frequency):
        """
        Finds the frequency of given parse result frequency.

        For frequency 0, this method should not be used!

        @type unigram_collection: Collection
        @type frequency: int
        @rtype: int
        """
        assert frequency and frequency > 0

        emission_key = "emission_key_val:this.item_0.word.parse_result.value"

        filter_criteria = {"value.count": frequency}
        return cls._find_count(unigram_collection, emission_key, filter_criteria)

    @classmethod
    def find_frequency_of_word_frequency(cls, unigram_collection, frequency):
        """
        Finds the frequency of given word frequency.

        For frequency 0, this method should not be used!

        @type unigram_collection: Collection
        @type frequency: int
        @rtype: int
        """
        assert frequency and frequency > 0

        emission_key = "emission_key_val:this.item_0.word.surface.value"

        filter_criteria = {"value.count": frequency}
        return cls._find_count(unigram_collection, emission_key, filter_criteria)

    @classmethod
    def find_distinct_count(cls, collection, ngram_type):
        """
        Finds the count of distinct items for ngram_type.

        @type collection: Collection
        @type ngram_type: list
        @rtype: int
        """

        emission_keys = cls._create_emission_keys(ngram_type)

        return cls._find_count(collection, emission_keys, None)

    @classmethod
    def find_distinct_word_count(cls, unigram_collection):
        """
        Finds the count of distinct words.
        @type unigram_collection:Collection
        @rtype: int
        """
        emission_key = "emission_key_val:this.item_0.word.surface.value"

        return cls._find_count(unigram_collection, emission_key, None)

    @classmethod
    def find_distinct_parse_result_count(cls, unigram_collection):
        """
        Finds the count of distinct parse results.
        @type unigram_collection:Collection
        @rtype: int
        """
        emission_key = "emission_key_val:this.item_0.word.parse_result.value"

        return cls._find_count(unigram_collection, emission_key, None)

    @classmethod
    def _find_count(cls, collection, emission_keys, filter_criteria):
        mapper = Code("""
                    function(){
                        emit({
                            """ + emission_keys + """
                        }, {count: 1});
                    }
                """)
        reducer = Code("""
                    function(key,values){
                        var total = 0;
                        for (var i = 0; i < values.length; i++) {
                            total += values[i].count
                        }

                        return {count:total};
                    }
                """)
        result = collection.map_reduce(mapper, reducer, "_temporary")

        if filter_criteria:
            result = result.find(filter_criteria)

        return result.count()

    @classmethod
    def _create_emission_keys(cls, ngram_type):
        emission_keys = ''

        for i, ngram_type_item in enumerate(ngram_type):
            emission_keys += "emission_key_val{}:this.item_{}.word.{}.value, ".format(i, i, ngram_type_item)
            emission_keys += "emission_key_cat{}:this.item_{}.word.{}.syntactic_category, ".format(i, i, ngram_type_item)

            # will be something like
            #emission_key_val0:this.item_0.word.surface.value, emission_key_cat0:this.item_0.word.surface.syntactic_category
            #emission_key_val1:this.item_1.word.surface.value, emission_key_cat1:this.item_1.word.surface.syntactic_category
            #emission_key_val2:this.item_2.word.stem.value,    emission_key_cat2:this.item_2.word.stem.syntactic_category
        return emission_keys