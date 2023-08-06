#include <stdexcept>
#include <iostream>
#include <regex>
#include <fstream>      // std::ifstream

#include <sys/types.h>
#include<iostream>

#ifdef _WIN32

#include <process.h> // For getpid on Windows

#endif


#include "text_file_processor.hpp"

using namespace std;

bool PriceQtyMissingDataHandler::call(shared_ptr<Record> record) {
    shared_ptr<QuotePairRecord> quote_pair = dynamic_pointer_cast<QuotePairRecord>(record);
    if (quote_pair) {
        if (quote_pair->bid_qty == 0) quote_pair->bid_qty = NAN;
        if (quote_pair->bid_price == 0) quote_pair->bid_price = NAN;
        if (quote_pair->ask_qty == 0) quote_pair->ask_qty = NAN;
        if (quote_pair->ask_price == 0) quote_pair->ask_price = NAN;
        return true;
    }
    
    shared_ptr<QuoteRecord> quote = dynamic_pointer_cast<QuoteRecord>(record);
    if (quote) {
        if (quote->qty == 0) quote->qty = NAN;
        if (quote->price == 0) quote->price = NAN;
        return true;
    }
    shared_ptr<TradeRecord> trade = dynamic_pointer_cast<TradeRecord>(record);
    if (trade) {
        bool ret = true;
        if (trade->qty == 0) {
            trade->qty = NAN;
            ret = false;
        }
        if (trade->price == 0) {
            trade->price = NAN;
            ret = false;
        }
        return ret;
    }
    shared_ptr<OpenInterestRecord> oi = dynamic_pointer_cast<OpenInterestRecord>(record);
    if (oi) {
        if (oi->qty == 0) oi->qty = NAN;
        return true;
    }
    return true;
}

PrintBadLineHandler::PrintBadLineHandler(bool raise) : _raise(raise) {}

shared_ptr<Record> PrintBadLineHandler::call(int line_number, const std::string& line, const std::exception& ex) {
    cerr << "parse error: " << ex.what() << " line number: " << line_number << " line: " << line << endl;
    if (_raise) throw ex;
    return nullptr;
}


RegExLineFilter::RegExLineFilter(const std::string& pattern) : _pattern (pattern) {}
    
bool RegExLineFilter::call(const std::string& line) {
    return std::regex_match(line, _pattern);
}

SubStringLineFilter::SubStringLineFilter(const vector<std::string>& patterns) :
    _patterns(patterns) {}

bool SubStringLineFilter::call(const std::string& line) {
    int size = static_cast<int>(line.size());
    for (int i = 0; i < size; ++i) {
        for (auto pattern : _patterns) {
            bool found = true;
            int k = 0;
            for (int j = 0; j < static_cast<int>(pattern.size()); ++j) {
                if (line[i + k] != pattern[j] || (i + k) == size) {
                    found = false;
                    break;
                }
                ++k;
            }
            if (found) return true;
        }
    }
    return false;
}

IsFieldInList::IsFieldInList(int flag_idx, const std::vector<std::string>& flag_values) :
    _flag_idx(flag_idx), _flag_values(flag_values) {}

bool IsFieldInList::call(const vector<string>& fields) {
    const std::string& val = fields[_flag_idx];
    return (std::find(_flag_values.begin(), _flag_values.end(), val) != _flag_values.end());
}

TextFileProcessor::TextFileProcessor(
                                    RecordGenerator* record_generator,
                                    LineFilter* line_filter,
                                    RecordParser* record_parser,
                                    BadLineHandler* bad_line_handler,
                                    RecordFilter* record_filter,
                                    MissingDataHandler* missing_data_handler,
                                    vector<Aggregator*> aggregators,
                                    int skip_rows) :
_record_generator(record_generator),
_line_filter(line_filter),
_record_parser(record_parser),
_bad_line_handler(bad_line_handler),
_record_filter(record_filter),
_missing_data_handler(missing_data_handler),
_aggregators(aggregators),
_skip_rows(skip_rows){}

int TextFileProcessor::call(const std::string& input_filename, const std::string& compression) {
#ifdef _WIN32
    cout << "processing file: " << input_filename << " process id: " << _getpid() << endl;
#else
    cout << "processing file: " << input_filename << " process id: " << getpid() << endl;
#endif
    shared_ptr<LineReader> istr = _record_generator->call(input_filename, compression);
    string line;
    int line_number = 0;
    while (istr->call(line)) {
        line_number++;
        //if (line_number > 200000) break;
        if (line_number <= _skip_rows) continue;
        if (_line_filter && !_line_filter->call(line)) continue;
        _record_parser->add_line(line);
        for (;;) {
            auto record = shared_ptr<Record>();
            try {
                record  = _record_parser->parse();
                if (!record) break;
            } catch(const ParseException& ex) {
                record = _bad_line_handler->call(line_number, line, ex);
                if (!record) continue;
            }
            if (_record_filter && !_record_filter->call(*record)) continue;
            if ((_missing_data_handler) && (!_missing_data_handler->call(record))) continue;
            for (auto aggregator : _aggregators) {
                aggregator->call(record.get(), line_number);
            }
        }
    }
    return line_number;
}
