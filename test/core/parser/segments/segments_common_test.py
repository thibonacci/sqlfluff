"""Test the KeywordSegment and EphemeralSegment classes."""

import pytest

from sqlfluff.core.parser import KeywordSegment, StringParser
from sqlfluff.core.parser.context import ParseContext
from sqlfluff.core.parser.segments import EphemeralSegment
from sqlfluff.core.parser.segments.base import UnparsableSegment


# NOTE: For legacy reasons we override this fixture for this module
@pytest.fixture(scope="module")
def raw_seg_list(generate_test_segments):
    """A generic list of raw segments to test against."""
    return generate_test_segments(["bar", "foo", "bar"])


def test__parser__core_keyword(raw_seg_list):
    """Test the Mystical KeywordSegment."""
    # First make a keyword
    FooKeyword = StringParser("foo", KeywordSegment, type="bar")
    # Check it looks as expected
    assert FooKeyword.template.upper() == "FOO"
    ctx = ParseContext(dialect=None)
    # Match it against a list and check it doesn't match
    assert not FooKeyword.match(raw_seg_list, parse_context=ctx)
    # Match it against a the first element and check it doesn't match
    assert not FooKeyword.match(raw_seg_list[0], parse_context=ctx)
    # Match it against a the first element as a list and check it doesn't match
    assert not FooKeyword.match([raw_seg_list[0]], parse_context=ctx)
    # Match it against the final element (returns tuple)
    m = FooKeyword.match(raw_seg_list[1], parse_context=ctx)
    assert m
    assert m.matched_segments[0].raw == "foo"
    assert isinstance(m.matched_segments[0], KeywordSegment)
    # Match it against the final element as a list
    assert FooKeyword.match([raw_seg_list[1]], parse_context=ctx)
    # Match it against a list slice and check it still works
    assert FooKeyword.match(raw_seg_list[1:], parse_context=ctx)
    # Check that the types work right. Importantly that the "bar"
    # type makes it in.
    assert m.matched_segments[0].class_types == {"base", "keyword", "raw", "bar"}


def test__parser__core_ephemeral_segment(raw_seg_list):
    """Test the EphemeralSegment."""
    # First make a keyword
    BarKeyword = StringParser("bar", KeywordSegment)

    ephemeral_segment = EphemeralSegment(
        segments=raw_seg_list[:1],
        pos_marker=None,
        parse_grammar=BarKeyword,
        ephemeral_name="foo",
    )

    ctx = ParseContext(dialect=None)
    # Parse it and make sure we don't get an EphemeralSegment back
    res = ephemeral_segment.parse(ctx)
    assert isinstance(res, tuple)
    elem = res[0]
    assert not isinstance(elem, EphemeralSegment)
    assert isinstance(elem, KeywordSegment)


def test__parser__core_ephemeral_unparsable(raw_seg_list):
    """Test the unparsable EphemeralSegment."""
    # First make a keyword
    TestKeyword = StringParser("somethingwedonthave", KeywordSegment)

    ephemeral_segment = EphemeralSegment(
        segments=raw_seg_list[:1],
        pos_marker=None,
        parse_grammar=TestKeyword,
        ephemeral_name="foo",
    )

    ctx = ParseContext(dialect=None)
    # Parse it and make sure we don't get an EphemeralSegment back
    res = ephemeral_segment.parse(ctx)
    assert isinstance(res, tuple)
    elem = res[0]
    # We should get an unparsable back.
    assert isinstance(elem, UnparsableSegment)
    # Check the ephemeral name comes through in the expectation.
    assert "Expected: 'foo'" in elem.stringify()
