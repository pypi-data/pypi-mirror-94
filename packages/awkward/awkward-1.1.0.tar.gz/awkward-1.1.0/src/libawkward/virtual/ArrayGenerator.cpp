// BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

#define FILENAME(line) FILENAME_FOR_EXCEPTIONS("src/libawkward/virtual/ArrayGenerator.cpp", line)

#include "sstream"

#include "awkward/array/VirtualArray.h"

#include "awkward/virtual/ArrayGenerator.h"

namespace awkward {
  ArrayGenerator::ArrayGenerator(const FormPtr& form, int64_t length)
      : form_(form)
      , length_(length) { }

  ArrayGenerator::~ArrayGenerator() = default;

  const FormPtr
  ArrayGenerator::form() const {
    if (form_.get() == nullptr  &&  inferred_form_.get() != nullptr) {
      return inferred_form_;
    }
    return form_;
  }

  int64_t
  ArrayGenerator::length() const {
    return length_;
  }

  const ContentPtr
  ArrayGenerator::generate_and_check() {
    ContentPtr out = generate();
    if (length_ >= 0  &&  length_ > out.get()->length()) {
      throw std::invalid_argument(
          std::string(
              "generated array does not have sufficient length: expected") +
          std::to_string(length_) + std::string(" but generated ") +
          std::to_string(out.get()->length()) + FILENAME(__LINE__));
    }
    if (form_.get() != nullptr  &&
        !form_.get()->equal(out.get()->form(true), true, true, false, true)) {
      throw std::invalid_argument(
          std::string("generated array does not conform to expected form:\n\n")
          + form_.get()->tostring() + std::string("\n\nbut generated:\n\n")
          + out.get()->form(true).get()->tostring() + FILENAME(__LINE__));
    }
    if (form_.get() == nullptr) {
      inferred_form_ = out.get()->form(true);
    }
    return out;
  }

  SliceGenerator::SliceGenerator(const FormPtr& form,
                                 int64_t length,
                                 const ContentPtr& content,
                                 const Slice& slice)
      : ArrayGenerator(form, length)
      , content_(content)
      , slice_(slice) { }

  const ContentPtr
  SliceGenerator::content() const {
    return content_;
  }

  const Slice
  SliceGenerator::slice() const {
    return slice_;
  }

  const ContentPtr
  SliceGenerator::generate() const {
    if (slice_.length() == 1) {
      SliceItemPtr head = slice_.head();
      if (SliceRange* raw = dynamic_cast<SliceRange*>(head.get())) {
        if (raw->step() == 1) {
          if (VirtualArray* a = dynamic_cast<VirtualArray*>(content_.get())) {
            return a->array().get()->getitem_range(raw->start(), raw->stop());
          }
          else {
            return content_.get()->getitem_range(raw->start(), raw->stop());
          }
        }
      }
    }
    if (VirtualArray* a = dynamic_cast<VirtualArray*>(content_.get())) {
      return a->array().get()->getitem(slice_);
    }
    else {
      return content_.get()->getitem(slice_);
    }
  }

  void
  SliceGenerator::caches(std::vector<ArrayCachePtr>& out) const {
    content_.get()->caches(out);
  }

  const std::string
  SliceGenerator::tostring_part(const std::string& indent,
                                const std::string& pre,
                                const std::string& post) const {
    std::stringstream out;
    out << indent << pre << "<SliceGenerator>\n";
    out << indent << "    <slice>" << slice_.tostring() << "</slice>\n";
    out << content_.get()->tostring_part(
             indent + std::string("    "), "<content>", "</content>\n");
    if (length_ >= 0) {
      out << indent << "    <length>" << length_ << "</length>\n";
    }
    if (form_.get() != nullptr) {
      std::string formstr = form_.get()->tojson(true, false);
      std::string replace = std::string("\n")
                                + indent + std::string("        ");
      size_t pos = 0;
      while ((pos = formstr.find("\n", pos)) != std::string::npos) {
        formstr.replace(pos, 1, replace);
        pos += replace.length();
      }
      out << indent << "    <form>\n" << indent << "        " << formstr
          << "\n" << indent << "    </form>\n";
    }
    out << indent << "</SliceGenerator>" << post;
    return out.str();
  }

  const std::shared_ptr<ArrayGenerator>
  SliceGenerator::shallow_copy() const {
    return std::make_shared<SliceGenerator>(form_,
                                            length_,
                                            content_,
                                            slice_);
  }

  const std::shared_ptr<ArrayGenerator>
  SliceGenerator::with_form(const FormPtr& form) const {
    return std::make_shared<SliceGenerator>(form,
                                            length_,
                                            content_,
                                            slice_);
  }

  const std::shared_ptr<ArrayGenerator>
  SliceGenerator::with_length(int64_t length) const {
    return std::make_shared<SliceGenerator>(form_,
                                            length,
                                            content_,
                                            slice_);
  }

  bool
  SliceGenerator::referentially_equal(const ArrayGeneratorPtr& other) const {
    if (length_ != other.get()->length()) {
      return false;
    }

    if (form_.get() == nullptr  &&  other.get()->form().get() != nullptr) {
      return false;
    }
    if (form_.get() != nullptr  &&  other.get()->form().get() == nullptr) {
      return false;
    }
    if (form_.get() != nullptr  &&  other.get()->form().get() != nullptr) {
      return form_.get()->equal(other.get()->form(), true, true, true, false);
    }

    if (length_ < 0  &&  other.get()->length() >= 0) {
      return false;
    }
    if (length_ >= 0  &&  other.get()->length() < 0) {
      return false;
    }
    if (length_ >= 0  &&  other.get()->length() >= 0  &&  length_ != other.get()->length()) {
      return false;
    }

    if (SliceGenerator* raw = dynamic_cast<SliceGenerator*>(other.get())) {
      return slice_.referentially_equal(raw->slice())  &&
             content_.get()->referentially_equal(raw->content());
    }
    else {
      return false;
    }
  }
}
