#ifndef aggregators_hpp
#define aggregators_hpp

#include <string>
#include <map>
#include <cmath>
#include <tuple>

#include "utils.hpp"
#include "pq_types.hpp"


int64_t parse_frequency(const std::string& frequency_str);

class SymbolTradeBar final {
public:
    SymbolTradeBar (std::shared_ptr<Writer>, const std::string& id, int64_t frequency);
    void add_trade(const TradeRecord& trade, int line_number);
    void close();
    ~SymbolTradeBar();
private:
    void write_records();
    void write_record(int line_number);
    void init_bar(const TradeRecord& trade);
    void update_bar(const TradeRecord& trade);
    std::shared_ptr<Tuple> get_curr_row();
    
    std::shared_ptr<Writer> _writer;
    std::string _id;
    int64_t _frequency;
    int64_t _last_update;
    float _o;
    float _h;
    float _l;
    float _c;
    float _v;
    float _total_volume;
    float _price_volume;
    int _time_unit;
    int _line_number;
    int _written_line_number;
    std::vector<std::pair<int, std::shared_ptr<Tuple>>> _records;
    bool _closed;
};

class TradeBarAggregator final : public Aggregator {
public:
    TradeBarAggregator(WriterCreator*, const std::string& frequency = "5m", Schema::Type timestamp_unit = Schema::TIMESTAMP_MILLI);
    void call(const Record* trade, int line_number) override;
    void close();
    ~TradeBarAggregator();
private:
    std::shared_ptr<Writer> _writer;
    int64_t _frequency;
    std::map<std::string, std::shared_ptr<SymbolTradeBar>> _trade_bars_by_symbol;
 };

class SymbolQuoteTOB final {
public:
    SymbolQuoteTOB(std::shared_ptr<Writer>, const std::string& id, int64_t frequency);
    void add_quote(const QuoteRecord& quote, int line_number);
    void close();
    ~SymbolQuoteTOB();
private:
    std::shared_ptr<Tuple> get_curr_row();
    void write_record(int line_number);
    void update_row(const QuoteRecord& trade);
    void write_records();

    std::shared_ptr<Writer> _writer;
    std::string _id;
    int64_t _timestamp;
    int64_t _last_update;
    float _bid;
    float _ask;
    float _bid_size;
    float _ask_size;
    int64_t _frequency;
    int _time_unit;
    int _line_number;
    int _written_line_number;
    std::vector<std::pair<int, std::shared_ptr<Tuple>>> _records;
    bool _closed;
};

class QuoteTOBAggregator final : public Aggregator {
public:
    //Assumes quotes are processed in time order.  Set frequency to "" to create bid / offer every time TOB changes.
    QuoteTOBAggregator(WriterCreator*, const std::string& frequency = "5m", Schema::Type timestamp_unit = Schema::TIMESTAMP_MILLI);
    void call(const Record* quote, int line_number) override;
    void close();
    ~QuoteTOBAggregator();
private:
    std::shared_ptr<Writer> _writer;
    int64_t _frequency;
    std::map<std::string, std::shared_ptr<SymbolQuoteTOB>> _tob_by_symbol;
};

class AllQuoteAggregator final : public Aggregator {
public:
    AllQuoteAggregator(WriterCreator*, Schema::Type timestamp_unit = Schema::TIMESTAMP_MILLI);
    void call(const Record* quote, int line_number) override;
private:
    std::shared_ptr<Writer> _writer;
    std::string _id;
    int _line_number_offset;
};

class AllQuotePairAggregator final : public Aggregator {
public:
    AllQuotePairAggregator(WriterCreator*, Schema::Type timestamp_unit = Schema::TIMESTAMP_MILLI);
    void call(const Record* quote, int line_number) override;
private:
    //std::string _id;
    WriterCreator* _writer_creator;
    Schema _schema;
    std::map<std::string, std::shared_ptr<Writer>> _writers;
};

class AllTradeAggregator final : public Aggregator {
public:
    AllTradeAggregator(WriterCreator*, Schema::Type timestamp_unit = Schema::TIMESTAMP_MILLI);
    void call(const Record* trade, int line_number) override;
private:
    //std::string _id;
    WriterCreator* _writer_creator;
    Schema _schema;
    std::map<std::string, std::shared_ptr<Writer>> _writers;
};

class AllOpenInterestAggregator final : public Aggregator {
public:
    AllOpenInterestAggregator(WriterCreator*, const Schema::Type timestamp_unit = Schema::TIMESTAMP_MILLI);
    void call(const Record* oi, int line_number) override;
private:
    std::shared_ptr<Writer> _writer;
    std::string _id;
};

class AllOtherAggregator final : public Aggregator {
public:
    AllOtherAggregator(WriterCreator*, Schema::Type timestamp_unit = Schema::TIMESTAMP_MILLI);
    void call(const Record* other, int line_number) override;
private:
    std::shared_ptr<Writer> _writer;
    std::string _id;
};



#endif
