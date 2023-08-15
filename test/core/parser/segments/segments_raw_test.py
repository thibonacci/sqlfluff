"""Test the RawSegment class."""

from sqlfluff.core.parser.segments.base import PathStep


def test__parser__raw_get_raw_segments(raw_seg_list):
    """Test niche case of calling get_raw_segments on a raw segment."""
    for s in raw_seg_list:
        assert s.get_raw_segments() == [s]


def test__parser__raw_segments_with_ancestors(
    raw_seg_list, DummySegment, DummyAuxSegment
):
    """Test raw_segments_with_ancestors.

    This is used in the reflow module to assess parse depth.
    """
    test_seg = DummySegment([DummyAuxSegment(raw_seg_list[:1]), raw_seg_list[1]])
    # Result should be the same raw segment, but with appropriate parents
    assert test_seg.raw_segments_with_ancestors == [
        (
            raw_seg_list[0],
            [
                PathStep(test_seg, 0, 2, (0, 1)),
                PathStep(test_seg.segments[0], 0, 1, (0,)),
            ],
        ),
        (raw_seg_list[1], [PathStep(test_seg, 1, 2, (0, 1))]),
    ]
