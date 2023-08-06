//! Global constants, such as compiler version used, algorithms, compression and filters supported and others

pub const COMPILATION_DATE: &str = "Feb 09 2021";
pub const COMPILATION_TIME: &str = "14:39:14";
pub const VERSION: &str = "0.4.10";
pub const ALGORITHMS: [&str; 10] = ["alpha","multiplicative","source_over","destination_over","mask_top","first_top","first_bottom","disjoint_over","disjoint_under","disjoint_debug"];
pub const COMPILER: &str = "rustc";
pub const COMPILER_VERSION: &str = "1.44.1";
pub const LIBPNG_VERSION: &str = "image-0.23";
pub const FEATURES: [&str; 2] = ["cpu","python"];
pub const PLATFORM_CPU_BITS: &str = "64";
pub const FILTER_TYPES: [image::codecs::png::FilterType; 5] = [image::codecs::png::FilterType::NoFilter,image::codecs::png::FilterType::Avg,image::codecs::png::FilterType::Paeth,image::codecs::png::FilterType::Sub,image::codecs::png::FilterType::Up];
pub const COMPRESSION_TYPES: [image::codecs::png::CompressionType; 5] = [image::codecs::png::CompressionType::Default,image::codecs::png::CompressionType::Best,image::codecs::png::CompressionType::Fast,image::codecs::png::CompressionType::Huffman,image::codecs::png::CompressionType::Rle];
pub const DEFAULT_THREAD_POOL_SIZE: usize = 2;
pub const MAX_THREAD_POOL_SIZE: usize = 20;
